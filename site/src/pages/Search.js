import React, { useState, useEffect } from 'react';
import {withRouter} from 'react-router-dom'
import Nav from '../fragments/Nav'
import Datatable from '../fragments/Datatable';
import AvailabilitySummary from '../fragments/AvailabilitySummary';
import PromptForm from '../fragments/PromptForm';


function Search() {

    const [data, setData] = useState({
        'locations': [],
        'location_stats': [], 
        'vax_stats': {}, 
    });
    
    const [params, setParams] = useState({
        'zip_': '78741',
        'radius': 50
    });
    
    const apiBase = 'https://p6ccqa7dik.execute-api.us-east-1.amazonaws.com/dev'
    const searchEndpoint = `${apiBase}/search`

    useEffect(() => {
        fetch(searchEndpoint, {
            method: 'POST',
            body: JSON.stringify(params)
        })
        .then(response => response.json())
        .then((json) => setData(json))
    }, []);

    
    return (
        <div className='container'>
            <Nav/>
            <div className='main'>
               <h6>Availability Summary for {params.zip_} + {params.radius} miles:</h6>
                <AvailabilitySummary className='card' data={data.vax_stats}/>
                {/* <Datatable data={data.location_stats}/> */}
                {/* <h6>Locations:</h6> */}
                <div style={{height: '40vh', overflow: 'scroll'}}>
                    <Datatable data={data.locations}/>
                </div>
                <PromptForm/>
            </div>
        </div>
    );
    

};

export default withRouter(Search)