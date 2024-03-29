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
##import  numpy               as  np
##import  matplotlib.pyplot   as  plt

# ================================================================================================= #
# Variables
# ================================================================================================= #


# USER MUST CHANGE THIS --------------------------------------------------------------------------- #
input_filename                  = 'P6.gcode'
target_layers                   = [5,9,13,16,17,18]
squish_percentage               = [0.50,0.50,0.50,0.50,0.50,0.50]
# ------------------------------------------------------------------------------------------------- #

input_filename_wo_extension     = input_filename[ :input_filename.find('.') ]                       # extract input filename without extension
extension                       = 'gcode'                                                           # define extension... may never need changing
output_filename                 = '{}_out_2.{}'.format( input_filename_wo_extension, extension )      # generate output filename to avoid overwriting


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
    layers                          = []
    mod_indeces                     = []
    mod_lines                       = []
    for i in range( 0, Nlines ):

        if lines[i][0:7] == '; layer':
            remove_semi_colon = lines[i].strip(';')
            split_by_comma = remove_semi_colon.split(',')
            try:
                layer_number        = int(      split_by_comma[0].split(' ')[2]             )
                z_height            = float(    split_by_comma[1].split(' ')[3][:-1]        )
            except:
                pass

            ddp = 0
            if layer_number >= layer:
                if layer_number >= 10:
                    ddp = 1
                mod_val             =  round(   z_height - ( layer_height*percentage ), 4   )
                mod_str             =  '{}{}\n'.format( lines[i][:(15+ddp)], str( mod_val ) )
                mod_indeces.append( i           )
                mod_lines.append(   mod_str     )
                layers.append(  (   layer_number, z_height, mod_val) )
                
                print( '[{:0.6f}] \t {} \t {} \t {}'.format( current_time(start_time), layer_number, z_height, mod_val ) )

            elif layer_number < layer:
                mod_lines.append(   lines[i]    )
                layers.append(  (   layer_number, z_height, z_height) )
                print( '[{:0.6f}] \t {} \t {} \t {}'.format( current_time(start_time), layer_number, z_height, z_height ) )
            
        else:
            mod_lines.append(       lines[i]    )
    
    # --------------------------------------------------------------------------------------------- # output/return
    return mod_indeces, mod_lines, layers

# ------------------------------------------------------------------------------------------------- #

def squish_layers_2( lines, input_layer, percentage ):
    '''
    Reduces selected layers by a specific percentage
    '''

    print( '[{:0.6f}] Squishing!'.format( current_time(start_time) ) )

    # --------------------------------------------------------------------------------------------- # defining variables
    layer_def_index                 = []                                                            # ...indeces where layer definitions are made
    mod_lines_index                 = []
    orig_lines                      = []
    orig_z                          = []
    mod_lines                       = []
    mod_z                           = []
    Nlines                          = len(lines)
    out_lines                       = lines

    # --------------------------------------------------------------------------------------------- # determining layer height programatically
    for i in range( 0, Nlines ):                                                                    # find layer height
        if lines[i][4:15] == 'layerHeight':
            layer_height            = float( lines[i][17:] )
            print( '[{:0.6f}] GCODE Layer Height set to = {}'.format( current_time(start_time), layer_height ) )
            break

    # --------------------------------------------------------------------------------------------- # here we get the index of the layers
    for i in range( 0, Nlines ):
        if lines[i][0:7] == '; layer':
            layer_def_index.append( i )

    N_layer_def = len(layer_def_index)

    # --------------------------------------------------------------------------------------------- # here we mod the lines between the input layer and the end of the file
    for i in range( layer_def_index[input_layer-1], layer_def_index[N_layer_def-1] ):
        if lines[i][0:4] == 'G1 Z':
            mod_lines_index.append(     i                                                       )
            orig_lines.append(          lines[i]                                                )
            orig_z.append(              float( lines[i][4:9] )                                  )
            mod_z.append(               round(   orig_z[-1] - ( layer_height*percentage ), 4   ))
            mod_lines.append(           'G1 Z{:0.3f} {}'.format( mod_z[-1], lines[i][10:] )     )

    # --------------------------------------------------------------------------------------------- # generate all lines for output file
    N_mod_lines = len( mod_lines_index )
    out_lines = lines
    for i in range( 0, N_mod_lines ):
        out_lines[ mod_lines_index[i] ] = mod_lines[i]
    
    # --------------------------------------------------------------------------------------------- # output/return
    return out_lines, layer_def_index , mod_lines_index, orig_lines, orig_z, mod_lines, mod_z 

# ------------------------------------------------------------------------------------------------- #

def current_time( start_time ):
    '''
    Stopwatch type function
    '''
    current_time                    = time.time() - start_time
    return current_time

# ------------------------------------------------------------------------------------------------- #

def vis_layers( layers ):
    '''
    Visualization of squished lines
    '''

    bar_width                       = 0.35
    Nlayers                         = len( layers )
    part                            = {}

# ================================================================================================= #
# Program
# ================================================================================================= #

Nlayers                                     = len( target_layers )

start_time                                  = time.time()
input_file_obj, lines                       = read_gcode( input_filename )

if Nlayers == 1:
    out_lines, layer_def_index , mod_lines_index, orig_lines, orig_z, mod_lines, mod_z              = squish_layers_2( lines, target_layers[0], squish_percentage[0]        )
elif Nlayers > 1:
    for i in range( 0, Nlayers ):
        if i == 0:
            out_lines, layer_def_index , mod_lines_index, orig_lines, orig_z, mod_lines, mod_z      = squish_layers_2( lines, target_layers[i], squish_percentage[i]        )
        elif i > 0:
            out_lines, layer_def_index , mod_lines_index, orig_lines, orig_z, mod_lines, mod_z      = squish_layers_2( out_lines, target_layers[i], squish_percentage[i]    )

write_gcode( output_filename, out_lines )

# ------------------------------------------------------------------------------------------------- #

##Nx = 2
##Nlayers = len(layers)
##p = {}
##
##for h in range( 0, 2 ):
##    for i in range( 0, Nlayers - 1):
##        if h == 0:
##            if i == 0:
##                p[str(i)] = plt.bar(h, init_layers[i][h+1], 0.35)
##            elif i > 0:
##                p[str(i)] = plt.bar(h, ( init_layers[i][h+1] - init_layers[i-1][h+1] ), 0.35, bottom=layers[i-1][h+1])
##        elif h > 0:
##            if i == 0:
##                p[str(i)] = plt.bar(h, layers[i][h+1], 0.35)
##            elif i > 0:
##                p[str(i)] = plt.bar(h, ( layers[i][h+1] - layers[i-1][h+1] ), 0.35, bottom=layers[i-1][h+1])
##
##plt.xticks([0,1], ('G1', 'G2'))
##plt.yticks(np.arange(0, 2.0, 0.15))
##plt.grid(True, axis='y', linestyle=':')
##plt.show()
