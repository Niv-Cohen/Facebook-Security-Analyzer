import React from 'react';
import { CircularProgress } from '@material-ui/core';
import {connect} from 'react-redux';

const WaitingPage = ({thresholds ,header_text}) =>{

    return(
            <div className='jumbotron mt-5'>
                <div align='center'>
                    <h1 className='display-4'>{header_text}</h1>
                    <p className='lead'>This may take a few minutes</p>
                    <CircularProgress style={{alignSelf: 'center'}} size={200}/>
                </div>
            </div>
    )
}

const mapStateToProps = state => ({
    thresholds: state.network.thresholds
});

export default connect(mapStateToProps,{})(WaitingPage)
