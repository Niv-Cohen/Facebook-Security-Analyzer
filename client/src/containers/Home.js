import React from 'react';
import { Link } from 'react-router-dom';
import {connect} from 'react-redux';
import {scrap_network, create_filtered_graph} from '../actions/network'

const Home = ({user, create_filtered_graph, scrap_network, thresholds, err_msg}) => {


    const {connection,minimum_trust_value,selected_action} = thresholds
    const user_thresholds = thresholds.user;
    const {total_friends, age_of_account} = user_thresholds
    const {mutual_friends, friendship_duration}  = connection;
    thresholds = {minimum_trust_value,total_friends, age_of_account, mutual_friends, friendship_duration,selected_action}
    const scaned_user = ()=>(
        <>
        <Link className="btn btn-outline-primary"role='button' to='/network' 
        onClick={()=>create_filtered_graph(user,thresholds)}>Use Prev Scan</Link>
        <Link className="btn btn-outline-primary" onClick={()=>scrap_network(user,thresholds)} role='button'
        to='/network'>New Scan</Link>
        </>
        
           
    )

    const unscanned_user = ()=>(
        <>
        <p class='lead'>No Previous Scan Was Found</p>
        <Link class='btn btn-primary btn-lg' onClick={()=>scrap_network(user,thresholds)} role='button'
        to='/network'>New Scan</Link>
        </>
    )

    const guest = () =>(
        <>
        <p class='lead'>Login and Scan Your Account</p>
        <Link class='btn btn-primary btn-lg' to='/login' role='button'>Login</Link>
        </>
    )
    

    return(
        
    <div className='container'>
        <div className='jumbotron mt-5'>
            <h1 className='display-4'>How Secured Is Your Network?</h1>
            <p className='lead'>This is a platform created to prevent info leakage</p>
            <p className='lead'>Based on an ongoing research</p>
            <hr className='my-4' />
            <p>Hi there {user?user.name:'guest'}!</p>
            <div class="alert alert-danger" hidden={!err_msg} role="alert">
            {err_msg}
            </div>
            {
            user?user.network?
            scaned_user():
            unscanned_user():
            guest()
            }
        </div>
    </div>
    
)};

const mapStateToProps = state => ({
    user : state.auth.user,
    err_msg: state.network.err_msg,
    thresholds: state.network.thresholds
});

export default connect(mapStateToProps,{create_filtered_graph, scrap_network})(Home);