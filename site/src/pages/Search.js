import React, { useState, useEffect } from 'react';
import {withRouter} from 'react-router-dom'
import axios from 'axios'
import Nav from '../fragments/Nav'
import Datatable from '../fragments/Datatable';



function Search() {

    const [data, setData] = useState([]);
    

    const params = {
        'zip_': '78741',
        'radius': 100
    }

    const apiBase = 'https://p6ccqa7dik.execute-api.us-east-1.amazonaws.com/dev'
    const searchEndpoint = `${apiBase}/search`
    
    useEffect(() => {
        fetch(searchEndpoint, params)
        .then(response => response.json())
        .then((json) => setData(json))
    }, []);

    
    return (
        <div className='container'>
            <Nav/>
            <div className='main'>
                <Datatable data={data}/>
            </div>
        </div>
    );
    

};

export default withRouter(Search)