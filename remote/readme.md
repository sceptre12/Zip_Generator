# Remote Code blue print

Code in this folder is to be executed on remote systems

-   Client zip_grabber
    -   
    -   It will be assigned a set of zipCodes
    -   Using the set of zip codes it will download the webpage 
    and store it on the filesystem
    -   After it has downloaded all the zips it will then parse 
    each file and send the parsed information through socket io
    
-   Server zip_handler
    -
    -   Db related functions
        -   Setup a rethinkdb on the server 
        -   Init method should set up the db with zip tables per computer / server  
        -   Populate the db tables with equal amount of zips per table
    -   Socket server 
        -   Set up server with end points   
            -   Gets
                -        Send table name
            -   Sets
                -       Store Zip Info
                        Store Requestor Information

-   Objects
    -   
    - Zip_info
        -       {
                    zip: 33068,
                    state: fl,
                    coordinates: {
                        lat: 20,
                        long: 20
                    },
                    area: {
                        land_area: 10,
                        water_area: 3,
                        radius_coverage: 5.3
                    },
                    population:{
                        population: 560000,
                        pop_density: 1563
                    }
                }
        
        