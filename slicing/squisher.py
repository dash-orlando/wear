'''
squisher.py

LAYER SQUISHER
    - Developed for the WEAR project
    - Changes the Z heigh of the printer do enhance layer bonding

Authors:
    - Fluvio Lobo Fengolietto
    - Rimma Uysal
'''

# ================================================================================================= #
# Libraries and Modules
# ================================================================================================= #

import  os


# ================================================================================================= #
# Variables
# ================================================================================================= #


# USER MUST CHANGE THIS --------------------------------------------------------------------------- #
input_filename                  = 'P6.gcode'
# ------------------------------------------------------------------------------------------------- #

input_filename_wo_extension     = input_filename[ :input_filename.find('.') ]                       # extract input filename without extension
extension                       = 'gcode'                                                           # define extension... may never need changing
output_filename                 = '{}_out.{}'.format( input_filename_wo_extension, extension )      # generate output filename to avoid overwriting


# ================================================================================================= #
# Functions
# ================================================================================================= #

def read_gcode( filename ):
    '''
    Reads GCODE
    '''

    with open( filename, 'r' ) as f:
        lines = f.readlines()

    return lines


def write_gcode( filename, data ):
    '''
    Writes GCODE using input array of strings

        TO DO:
            - Add a check for file existance and erasing to avoid issues/errors
        
    '''

    if os.path.exists( filename ):
        print( "Output filename exists... will remove to avoid overwriting issues" )
        os.remove( filename )
    
    f = open( output_filename, 'a+' )

    for i in range( 0 , len(data) ):
        f.write( data[i] )

    f.close()


# ================================================================================================= #
# Program
# ================================================================================================= #


lines = read_gcode( input_filename )

data = ['hola','pp','hola']

write_gcode( output_filename, data )


'''
gcode = open( filename, 'r' )

print( gcode.read(10) )


# Definitions

squish = []
slayer = []
'''


