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
import  time

# ================================================================================================= #
# Variables
# ================================================================================================= #


# USER MUST CHANGE THIS --------------------------------------------------------------------------- #
input_filename                  = 'P6.gcode'
target_layers                   = [3,5]
squish_percentage               = [0.50,0.50]
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

    t = current_time(start_time)
    print( '[{:0.6f}] Reading GCODE'.format( t ) )
    
    with open( filename, 'r' ) as f:
        lines = f.readlines()

    return f, lines

# ------------------------------------------------------------------------------------------------- #

def write_gcode( filename, lines ):
    '''
    Writes GCODE using input array of strings
    '''

    t = current_time(start_time)
    print( '[{:0.6f}] Writing GCODE'.format( t ) )
    
    if os.path.exists( filename ):
        print( '[{:0.6f}] Existent output file will be removed'.format( t ) )
        os.remove( filename )
    
    f = open( output_filename, 'a+' )

    Nlines = len(lines)
    for i in range( 0 , Nlines ):
        f.write( lines[i] )

    f.close()

    return f

# ------------------------------------------------------------------------------------------------- #

def squish_layers( lines, layer, percentage ):
    '''
    Reduces selected layers by a specific percentage
    '''

    print( '[{:0.6f}] Squishing!'.format( current_time(start_time) ) )
    


    Nlines                          = len(lines)                                                    # calculate number of lines in input file/data structure
    for i in range( 0, Nlines ):                                                                    # find layer height
        if lines[i][4:15] == 'layerHeight':
            layer_height            = float( lines[i][17:] )
            print( '[{:0.6f}] GCODE Layer Height set to = {}'.format( current_time(start_time), layer_height ) )
            break


    # --------------------------------------------------------------------------------------------- # search for specific layer lines to modify
    mod_indeces                     = []
    mod_lines                       = []
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

            
                print( '[{:0.6f}] \t {} \t {} \t {}'.format( current_time(start_time), layer_number, z_height, mod_val ) )
            
        else:
            mod_lines.append(       lines[i] )

    # --------------------------------------------------------------------------------------------- # output/return
    return mod_indeces, mod_lines

# ------------------------------------------------------------------------------------------------- #

def current_time( start_time ):
    '''
    Stopwatch type function
    '''
    current_time                    = time.time() - start_time
    return current_time


# ================================================================================================= #
# Program
# ================================================================================================= #

Nlayers                             = len( target_layers )

start_time                          = time.time()
input_file_obj, lines               = read_gcode( input_filename )

if Nlayers == 1:
    mod_indeces, mod_lines          = squish_layers( lines, target_layers[0], squish_percentage[0] )
elif Nlayers > 1:
    for i in range( 0, Nlayers ):
        if i == 0:
            mod_indeces, mod_lines  = squish_layers( lines, target_layers[i], squish_percentage[i] )
        elif i > 0:
            mod_indeces, mod_lines  = squish_layers( mod_lines, target_layers[i], squish_percentage[i] )

write_gcode( output_filename, mod_lines )



