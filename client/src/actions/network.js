import axios from 'axios';
import Cookies from 'js-cookie';
import {
    SCRAP_SUCCESS,
    SCRAP_FAIL,
    FILTERED_GRAPH_SUCCESS,
    FILTER_FAIL,
    SCRAPPING,
    FILTERRING,
    FINISH_SCRAPPING,
} from './types';

export const create_filtered_graph = (user_state,thresholds) => async dispatch => {
    dispatch({
        type:FILTERRING,
        payload:thresholds
    })

    const config = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    };
    
    const {email} = user_state;
    console.log(thresholds)
    const  { mutual_friends, friendship_duration, total_friends, age_of_account,minimum_trust_value,selected_action } = thresholds;
    const body = JSON.stringify({email, mutual_friends, friendship_duration, total_friends, age_of_account, minimum_trust_value,selected_action });
    console.log(body)
    try {
        const res = await axios.post(`${process.env.REACT_APP_API_URL}/network/filter/`, body, config);
        if(res.status===200){
            dispatch({
                type: FILTERED_GRAPH_SUCCESS,
                payload: res.data
            });
        }else{
            dispatch({
                type: FILTER_FAIL,
                payload: 'Unable To Filter Network'
            })
        }
    }catch (err) {
        dispatch({
            type: FILTER_FAIL,
            payload: 'Unable To Filter Network'
        })
    }
};


export const scrap_network = (user_state,thresholds) => async dispatch => {
    dispatch({
        type:SCRAPPING
    })
    const config = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    };
    
    const {password,email,name} = user_state;
    const  {connection,user} = thresholds;
    const body = JSON.stringify({email,name,password, connection, user});
    
    try {
        const res = await axios.put(`${process.env.REACT_APP_API_URL}/network/scrap/`, body, config);
        if (res.status===200) {
            console.log(res.data)
            dispatch({
                type: SCRAP_SUCCESS,
                payload: res.data
            });
        } else {
            dispatch({
                type: SCRAP_FAIL,
                payload: 'Unable To Scan Network'
            })
        }
    } catch (err) {
        dispatch({
            type: SCRAP_FAIL,
            payload: 'Unable To Scan Network'
        })
    }
};

export const finish_scrapping = () => dispatch => {
    dispatch({
        type:FINISH_SCRAPPING
    })
}

