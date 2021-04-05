import React, { useState, useEffect } from 'react';
import { withRouter, useLocation } from 'react-router-dom'
import Nav from '../fragments/Nav'
import Datatable from '../fragments/Datatable';
import AvailabilitySummary from '../fragments/AvailabilitySummary';
import PromptForm from '../fragments/PromptForm';
import queryString from 'query-string'

function Search() {
    const { search } = useLocation() 
    const { zip, radius } = queryString.parse(search)
    const paramRadius = radius ? parseInt(radius) : 50
    const paramZip = zip ? zip : '78741' // remove this once form is in

    const [params, setParams] = useState({
        'zip_': paramZip,
        'radius': paramRadius
    });
    
    const [data, setData] = useState({
        'locations': [],
        'location_stats': [], 
        'vax_stats': {}, 
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
                {/* <PromptForm/> */}
            </div>
        </div>
    );
    

};

export default withRouter(Search)