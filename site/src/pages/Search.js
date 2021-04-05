import React, { Component, useState, useEffect } from 'react';

import Nav from '../fragments/Nav'
import Datatable from '../fragments/Datatable';

require("axios");

class Search extends Component {

    
    const [data, setData] = useState([]);
    // const [params, setParams] = useState({
    //     zip_: "78741",
    //     radius: 10

    // })
    useEffect(() => {
        fetch()
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