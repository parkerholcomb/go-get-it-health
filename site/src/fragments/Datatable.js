import React from "react";

function drawTd(val){
    if (val == 0) {
        return '-'
    } else {
        return val
    }
}

function getUnits(col) {
    if (col =='miles_away') {
        return ' mi.'
    }
}

export default function Datatable({ data }) {
    const columns = data[0] && Object.keys(data[0])
    return <table className='table table-striped' cellPadding={0} cellSpacing={0}>
        <thead>
            <tr>{data[0] && columns.map((heading) => <th>{heading}</th>)}</tr>
        </thead>
        <tbody>
            {data.map(row => <tr>
                {
                    columns.map(column => <td>{drawTd(row[column])}{getUnits(column)}</td>)
                }
            </tr>)}
        </tbody>
    </table>
}