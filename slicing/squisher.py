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
target_layers                   = [3,5,7]
squish_percentage               = 0.50
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

    return f, lines

# ------------------------------------------------------------------------------------------------- #

def write_gcode( filename, lines ):
    '''
    Writes GCODE using input array of strings
    '''

    if os.path.exists( filename ):
        print( '> Output filename exists... will remove to avoid overwriting issues' )
        os.remove( filename )
    
    f = open( output_filename, 'a+' )

    Nlines = len(lines)
    for i in range( 0 , Nlines ):
        f.write( lines[i] )

    f.close()

    return f

# ------------------------------------------------------------------------------------------------- #

def squish_layers( lines, layers, percentage ):
    '''
    Reduces selected layers by a specific percentage
    '''

    Nlines                          = len(lines)                                                    # calculate number of lines in input file/data structure

    for i in range( 0, Nlines ):                                                                    # find layer height
        if lines[i][4:15] == 'layerHeight':
            layer_height            = float( lines[i][17:] )
            print( '> GCODE Layer Height set to = {}'.format( layer_height ) )
            break


    # --------------------------------------------------------------------------------------------- # search for specific layer lines to modify
    mod_indeces                     = []
    mod_lines                       = []
    layer                           = 3
    for i in range( 0, Nlines ):

        if lines[i][0:7] == '; layer':
            remove_semi_colon = lines[i].strip(';')
            split_by_comma = remove_semi_colon.split(',')
            try:
                layer_number        = int(split_by_comma[0].split(' ')[2])
                z_height            = float( split_by_comma[1].split(' ')[3][:-1] )
            except:
                pass

            ddp = 0
            if layer_number >= layer:
                if layer_number >= 10:
                    ddp = 1
                mod_val             =  round( z_height - ( layer_height*percentage ), 4)
                mod_str             =  '{}{}\n'.format( lines[i][:(15+ddp)], str( mod_val ) )
                mod_indeces.append( i           )
                mod_lines.append(   mod_str     )

            
                print( layer_number, z_height, mod_val )
            
        else:
            mod_lines.append(   lines[i] )

    # --------------------------------------------------------------------------------------------- # output/return
    return mod_indeces, mod_lines        

# ================================================================================================= #
# Program
# ================================================================================================= #


input_file_obj, lines           = read_gcode( input_filename )

mod_indeces, mod_lines = squish_layers( lines, 3, squish_percentage )

write_gcode( output_filename, mod_lines )



