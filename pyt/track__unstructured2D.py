import numpy                    as np
import nkUtilities.plot1D       as pl1
import nkUtilities.load__config as lcf

# ========================================================= #
# ===  track__unstructured2D.py                         === #
# ========================================================= #

def track__unstructured2D():

    # ------------------------------------------------- #
    # --- [1] load parameters / data                --- #
    # ------------------------------------------------- #
    import nkUtilities.load__constants as lcn
    cnsFile  = "dat/parameter.conf"
    const    = lcn.load__constants( inpFile=cnsFile )
    
    import nkUtilities.load__pointFile as lpf
    Data     = lpf.load__pointFile( inpFile=const["fieldFile"], returnType="point" )
    points   = lpf.load__pointFile( inpFile=const["pointFile"], returnType="point" )

    x_,y_,v_ = const["xyv_index"]
    if   ( Data.shape[1] == 2 ):
        Data = np.concatenate( [ Data, np.zeros( Data.shape[0],1 ) ], axis=1 )
    elif ( Data.shape[1] == 3 ):
        Data = np.copy( Data )
    elif ( Data.shape[1] >= 4 ):
        Data = np.concatenate( [ Data[:,x_], Data[:,y_], Data[:,v_] ], axis=1 )
    else:
        sys.exit( "[track__unstructured2D.py] illegal shape field.... look at the contents of the const[fieldFile]. [ERROR]" )
        
    # ------------------------------------------------- #
    # --- [2] interpolation                         --- #
    # ------------------------------------------------- #
    import nkInterpolator.interpolate__triElement as tri
    ret = tri.interpolate__triElement( nodes=Data, points=points )

    # ------------------------------------------------- #
    # --- [3] save in a file                        --- #
    # ------------------------------------------------- #
    import nkUtilities.save__pointFile as spf
    spf.save__pointFile( outFile=const["outFile"], Data=ret )

    # ------------------------------------------------- #
    # --- [4] draw a graph                          --- #
    # ------------------------------------------------- #
    if ( const["plotGraph"] ):
        xl_,yl_,vl_ = 0, 1, 2
        slength = np.cumsum( np.insert( np.sqrt( np.sum( ( np.diff( ret[:,0:2], axis=0 ) )**2, axis=1 ) ), 0, 0 ) )
        print( slength.shape, ret.shape )
        config  = lcf.load__config()
        keys    = [ "plt_xAutoRange", "plt_yAutoRange", "plt_xRange", "plt_yRange" ]
        for key in keys: config[key] = const[key]
        
        fig     = pl1.plot1D( config=config, pngFile=const["pngFile"] )
        fig.add__plot( xAxis=slength, yAxis=ret[:,vl_] )
        fig.set__axis()
        fig.save__figure()
    
    

# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    test = True
    if ( test ):

        x_, y_, z_ = 0, 1, 2
        
        import nkUtilities.equiSpaceGrid as esg
        x1MinMaxNum = [ -1.0, 1.0, 51 ]
        x2MinMaxNum = [ -1.0, 1.0, 51 ]
        x3MinMaxNum = [  0.0, 0.0,  1 ]
        ret         = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                         x3MinMaxNum=x3MinMaxNum, returnType = "point" )
        # ret[:,z_]   = np.exp( - 0.5*( ret[:,x_]**2 + ret[:,y_]**2 ) )
        ret[:,z_]   = np.sqrt( ret[:,x_]**2 + ret[:,y_]**2 )

        import nkUtilities.save__pointFile as spf
        outFile     = "dat/field.dat"
        spf.save__pointFile( outFile=outFile, Data=ret )

        tvar        = np.linspace( 0.0, 1.0, 101 )
        pt1, pt2    = np.array( [0,0,0] ), np.array( [1,0,0] )
        pt3, pt4    = np.array( [0,1,0] ), np.array( [0,0,0] )
        pt1         = np.repeat( pt1[None,:], tvar.shape[0], axis=0 )
        pt2         = np.repeat( pt2[None,:], tvar.shape[0], axis=0 )
        pt3         = np.repeat( pt3[None,:], tvar.shape[0], axis=0 )
        pt4         = np.repeat( pt4[None,:], tvar.shape[0], axis=0 )
        tvar        = np.repeat( tvar[:,None], 3, axis=1 )
        line1       = pt1 + ( pt2 - pt1 ) * tvar
        line2       = pt2 + ( pt3 - pt2 ) * tvar
        line3       = pt3 + ( pt4 - pt3 ) * tvar
        points      = np.concatenate( [line1,line2,line3], axis=0 )
        
        import nkUtilities.save__pointFile as spf
        outFile     = "dat/points.dat"
        spf.save__pointFile( outFile=outFile, Data=points )

        
    track__unstructured2D()

        
    
