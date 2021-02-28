import {
    FILTERED_GRAPH_SUCCESS,
    SCRAP_SUCCESS,
    SCRAP_FAIL,
    SCRAPPING,
    FILTERRING,
    FILTER_FAIL,
    FINISH_SCRAPPING
} from '../actions/types';

const initialState = {
    is_scrapping: false,
    is_filtering: false,
    scrapped_network:null,
    err_msg:"",
    thresholds:{
        minimum_trust_value:0,
        selected_action:"Seeing Attributes",
        connection:{
            mutual_friends:10,
            friendship_duration:356
        },
        user:{
            total_friends:150,
            age_of_account:356
        }
    }
};

export default function(state = initialState, action) {
    const { type, payload } = action;

    switch(type) {
        case SCRAPPING:
            return{
                ...state,
                is_scrapping:true,
                err_msg:null
            }
        case FILTERRING:
            const  { mutual_friends, friendship_duration, total_friends, age_of_account,minimum_trust_value, selected_action } = payload;
            return{
                ...state,
                is_filtering:true,
                thresholds: 
                    {minimum_trust_value,
                     selected_action,
                     connection:{friendship_duration,mutual_friends},
                     user:{total_friends,age_of_account}},
                err_msg:null
            }
        case FILTERED_GRAPH_SUCCESS:
            return {
                ...state,
                is_filtering:false,
                
            }
        case SCRAP_SUCCESS:
            return {
                ...state,
                scrapped_network:payload
            }
        case SCRAP_FAIL:
            return {
                ...state,
                is_scrapping:false,
                err_msg:'Something went wrong with Scrapping the network'
            }
        case FILTER_FAIL:
             return {
                    ...state,
                    is_filtering:false,
                    err_msg:'Something went wrong with Scrapping the network'
             }
        case FINISH_SCRAPPING:
            return{
                ...state,
                is_scrapping:false,
                scrapped_network:null
            }
        default:
            return state
    }
};