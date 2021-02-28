import React from 'react'
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import { refresh_user } from '../actions/auth';
import {finish_scrapping} from '../actions/network'
import WaitingPage from '../components/WaitingPage'
import Network from '../components/Network'


const Scan = ({user,is_scrapping, scrapped_network, is_filtering, err_msg, refresh_user, finish_scrapping}) =>{
    if(scrapped_network){
        refresh_user(scrapped_network)
        finish_scrapping()
    }
   

    const scrap_text='We Are Scraping Your Network';
    const filter_text='We Are Creating Your Filtered Network'
    
    return (
        <div className='container'>
            {is_scrapping===true?
            <WaitingPage header_text={scrap_text}/>:
            is_filtering?
            <WaitingPage header_text={filter_text}/>:
            err_msg?
            <Redirect to='/'/>
            :
            <Network name={user.name}/>
            }
        </div>
    )
}


const mapStateToProps = state => ({
    user: state.auth.user,
    is_filtering: state.network.is_filtering,
    is_scrapping: state.network.is_scrapping,
    scrapped_network: state.network.scrapped_network,
    err_msg: state.network.err_msg,
    thresholds: state.network.thresholds
})


export default connect(mapStateToProps,{refresh_user,finish_scrapping})(Scan)