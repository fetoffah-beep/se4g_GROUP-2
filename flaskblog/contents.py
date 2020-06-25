def cont(): 
    contents = [
        {
            'title' : 'General Introduction',
            'isi' : '''Walking is the most basic yet an indispensable mode of transportation since the beginning of
                        human civilization. However, due to the increase in the number of vehicles and human population
                        within the urban areas, mobility of pedestrian is gradually becoming a global concern. While
                        facilitating modern means of transport, the importance of walking in terms of health benefits and
                        necessity should not be overlooked. Therefore, it is inevitable to provide required conditions for
                        pedestrians during road traffic planning in order to encourage the walking practice, otherwise,
                        pedestrians will be deprived from a smooth and safe movement under the influence of complex
                        motorized vehicular movement.'''
        },
        {
            'title' : 'Aim',
            'isi' : '''For the current project, the Pedestrian LOS Model is aimed at evaluating walking conditions on
                        some of the selected road and street corridors in Milan urban environment. In addition, the enhanced PLOS was 
                        culculated by considering additional pararameters, namely number of light, presence of curb ramp, 
                        crossing, transport stop, point of interest and public service.'''
        },
        {
            'title' : 'Tools',
            'isi' : '''Epicollect
                        QGis
                        GeoServer'''
        },
        {
            'title' : 'Data Collection and Processing',
            'isi' : '''During the project, field data was collected using Epicollet. the data was collected in point form
                        which was later transferred to QGis for further processing and analysis. Some of the in-put field
                        data collected include :
                        > Width of the Sidewalk
                        > Counts of Streetlights
                        > Width of the Buffer
                        > Parking Space
                        > Curb Ramps
                        The processing activity was undertaken to enrich each geometry of the road network layer with
                        missing indicators.'''
        },
        {
            'title' : 'Result',
            'isi' : '''Streets and sidewalk infrastructure with different characteristics can be evaluated with this PLOS
                        method as it includes the highly important sidewalk factors that are used to evaluate the service
                        quality of sidewalks that can be used in various contexts. From the analysis, the model is highly
                        sensitive to the width of the side walk and the PLOS values ranges from 1.09 to 2.93. By considering the 
                        additional parameters, the enhanced PLOS was derived from the original PLOS value. These parameters increases the 
                        walkability of some road segements.'''
        }
    ]
    return contents