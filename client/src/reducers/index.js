import { combineReducers } from 'redux';
import auth from './auth';
import network from './network';

export default combineReducers({
    auth,network
});