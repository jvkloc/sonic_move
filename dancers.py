# Class for storing sensor data of each Biodata Sonata dancer.
class Dancers:
    """ This class stores sensor data of each Biodata Sonata
    dancer for the dashboard plots.
    """
    def __init__(self):
        """Initialises Dancers object.
        Parameters
        --------------
        dancers : list
            List of dictionaries of dictionaries. Each of the three
            dancers has three sensors, each of the sensors has six
            different measurement data.
        """
        self.dancers = [
                {'snsr_1' : {} ,'snsr_2' : {}, 'snsr_3' : {}} for _ in range(3)
        ]
        # Length of data plots' x-axes is 500, initialise data as zeros.
        for dancer in self.dancers:
                for i in range(1, 4):
                    dancer[f'snsr_{i}']['tot_a'] = [0]*500
                    dancer[f'snsr_{i}']['b_tot_a'] = [0]*500
                    dancer[f'snsr_{i}']['rot'] = [0]*500
                    dancer[f'snsr_{i}']['ori_p'] = [0]*500
                    dancer[f'snsr_{i}']['ori_r'] = [0]*500
                    dancer[f'snsr_{i}']['ori_y'] = [0]*500
                    for data in ['acc', 'gyr', 'mag']:
                        for axis in ['x', 'y', 'z']:
                            dancer[f'snsr_{i}'][f'{data}_{axis}'] = [0]*500
