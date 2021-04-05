import React from "react";

export default function AvailabilitySummary({ data }) {
    const keys = data && Object.keys(data)
    console.log(data);
    console.log(keys);
    return (
        <div style={{flexDirection: 'row', justifyContent: 'space-between', flexWrap: 'wrap', margin: "25px 0"}}>
            {data && keys.map((key) => <div style={{alignItems: "center", padding: '10px', width: '150px'}}>
                <div style={{fontSize: '1.25rem', padding: '10px'}}>{data[key]}</div>
                <div style={{fontSize: '.6rem'}}>{key}</div>
            </div>)}
        </div>
    )
}