import React from 'react'
import NetworkFilters from './NetworkFilters'

const Network = ({name})=>{
    return(
        <>
        <div class="text-center">
        {/* <img src={require('../assets/'+name+'.png')} width="700" height="60%"/> */}
        {/* <iframe src={'../assets/'+name+'.html'} height="500" width="1000"></iframe> */}
        <NetworkFilters />
        </div>
        </>
    )
}

export default Network