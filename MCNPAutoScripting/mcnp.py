from .extra import fold128
from . import Surfaces

default_density = 'weight'
default_importance = 'imp:n,p 1'
default_energy_string = '0 1e-5 932i 8.4295'

def densitytype(density_type):
    if density_type == 'weight':
        return -1
    elif density_type == 'atomic':
        return 1
    else:
        raise ValueError(f"Unknown density type: {density_type}")

class Cell:
    def __init__(self, cell_id, material_id, density, label=None, density_type=default_density, importance_string=default_importance, surface_string=''):
        self.cell_id = cell_id
        self.material_id = material_id
        self.density = density
        self.label = label
        self.density_type = density_type
        self.importance_string = importance_string
        self.surface_string = surface_string

    def string(self):
        _cmt = ''
        if self.label:
            _cmt = f"$ {self.label}"
        _dns = ''
        if self.density:
            _dns = f" {float(densitytype(self.density_type) * self.density)}"
        _str = f"{self.cell_id} {self.material_id}{_dns} {self.surface_string} {self.importance_string} {_cmt}"
        return fold128(_str)+"\n"
    
class Material:
    def __init__(self, material_id, elements, portions, density_type=default_density, labels=None, label=None):
        self.material_id = material_id

        self.elements = elements
        self.portions = portions
        self.density_type = density_type
        self.labels = labels
        self.label = label

    def string(self):
        portions = self.portions
        nonzero_indices = [i for i, portion in enumerate(portions) if portion != 0]
        elements = [self.elements[i] for i in nonzero_indices]
        portions = [self.portions[i] for i in nonzero_indices]
        _str = ''
        if self.label:
            _str += f"c {self.label}\n"
        _str += f"m{self.material_id}"
        for i, (elem, portion) in enumerate(zip(elements, portions)):
            _cmt = ''
            if self.labels:
                _cmt = f"$ {self.labels[i]}"
            _str += f"\t{elem} {densitytype(self.density_type) * portion} {_cmt}\n"
        return _str

class DetectorTally8:
    def __init__(
            self, 
            tally_id, 
            detector_cells, 
            geb=None,
            phl=None,
            energy_string=default_energy_string, 
            importance_string=':n,p', 
            label=None):
        
        self.geb = geb
        self.phl = phl
        self.tally_id = tally_id
        self.detector_cells = detector_cells
        self.energy_string = energy_string
        self.importance_string = importance_string
        self.label = label

    def string(self):
        _str = ''
        if self.label:
            _str = f"c {self.label}\n"
        _str += f"F{self.tally_id}{self.importance_string} "
        _str+='('
        for i, cell in enumerate(self.detector_cells):
            _str += f"{cell}"
            if i != len(self.detector_cells)-1:
                _str += ' '
        _str += f")\n"
        _str += f"E{self.tally_id} {self.energy_string}\n"
        if any([self.geb, self.phl]):
            _str += f"FT{self.tally_id}"
            if self.geb:
                _str += f" GEB {self.geb[0]} {self.geb[1]} {self.geb[2]}"
            if self.phl:
                _str += f" PHL {self.phl[0]} {self.phl[1]} {self.phl[2]} {self.phl[3]}"
            _str += '\n'


        return _str
    
class DetectorTally6:
    def __init__(self, tally_id, detector_cells, soil_cells=None, energy_string=default_energy_string, importance_string=':n,p', label=None):
        self.tally_id = tally_id
        self.detector_cells = detector_cells
        self.soil_cells = soil_cells
        self.energy_string = energy_string
        self.importance_string = importance_string
        self.label = label

    def string(self):
        _str = ''
        if self.label:
            _str = f"c {self.label}\n"
        _str += f"F{self.tally_id}{self.importance_string} "
        _str += '('
        for i, cell in enumerate(self.detector_cells):
            _str += f"{cell}"
            if i != len(self.detector_cells)-1:
                _str += ' '
        _str += f")\n"
        _str += f"E{self.tally_id} {self.energy_string}\n"
        if self.soil_cells:
            _fstr = f"FU{self.tally_id} "
            _fstr += ' '.join(map(str, self.soil_cells))
            _str += fold128(_fstr)+'\n'
        return _str
    
class SoilTally6:
    def __init__(self, tally_id, soil_cells, energy_string=default_energy_string, importance_string=":p,n", label=None):
        self.tally_id = tally_id
        self.soil_cells = soil_cells
        self.energy_string = energy_string
        self.importance_string = importance_string
        self.label = label

    def string(self):
        _str = ''
        if self.label:
            _str = f"c {self.label}\n"

        f_str = f"F{self.tally_id}{self.importance_string} "
        for i, cell in enumerate(self.soil_cells):
            f_str += f"{cell}"
            if i != len(self.soil_cells)-1:
                f_str += ' '
        _str += fold128(f_str)+'\n'
        _str += f"E{self.tally_id} {self.energy_string}\n"
        return _str

class Source:
    def __init__(self, energy_string = '14.0', position_string='0 0 0', direction_string = 'd1', vector_string='0 0 1', label=None, si_string='-1 .93 1', sp_string='0 0.0 1.0'):
        self.label = label
        self.energy_string = energy_string
        self.position_string = position_string
        self.direction_string = direction_string
        self.vector_string = vector_string
        self.si_string = si_string
        self.sp_string = sp_string

    def string(self):
        _str = f'sdef erg={self.energy_string} pos={self.position_string} dir={self.direction_string} vec={self.vector_string}\n'
        _str += f'si1 {self.si_string}\n'
        _str += f'sp1 {self.sp_string}\n'
        return _str

class MiscData:
    def __init__(self):
        pass

    def string(self):
        _str = """mode n p
prdmp 1e8 1e8 -1 $ dump every hour
Cut:n 1j 0.1 $ 100 keV Neutron Energy Cutoff
phys:n 1j 14 $analog neutron transport
phys:p
nps 1e9
"""
        return _str

class MCNP:
    def __init__(
            self, 
            title = "MCNP Simulation",
            cells=[], surfaces=[], 
            source=Source(), materials=[], 
            tallies=[], misc_data=[MiscData()]
            ):
        self.title = title
        self.cells = cells
        self.surfaces = surfaces
        self.source = source
        self.materials = materials
        self.tallies = tallies
        self.misc_data = misc_data

    def string(self):
        _str = ''
        _str += f"c {self.title}\n"
        _str += f"c ***CELLS***\n"
        for cell in self.cells:
            _str += cell.string()
        _str += '\n'
        _str +='c ***SURFACES***\n'
        for surface in self.surfaces:
            _str += surface.string()
        _str += '\n'

        _str +='c ***SOURCE***\n'
        _str += self.source.string()

        _str +='c ***MATERIALS***\n'
        for material in self.materials:
            _str += material.string()

        _str +='c ***TALLIES***\n'
        for tally in self.tallies:
            _str += tally.string()

        _str +='c ***DATA***\n'
        for misc in self.misc_data:
            _str += misc.string()

        if _str[-2:] == '\n':
            _str = _str[:-1]
        return _str