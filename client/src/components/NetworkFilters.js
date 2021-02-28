import React,{useState} from 'react'
import { create_filtered_graph } from '../actions/network';
import {connect} from 'react-redux';
import CSRFToken from './CSRFToken'

const actions = ['Seeing Posts', 'Seeing Pictures','Seeing Attributes', 'Commenting', 'Sharing', 'Tagging']

const NetworkFilters = ({user, thresholds, create_filtered_graph})=>{
    const [formData, setFormData] = useState({
        mutual_friends:thresholds.connection.mutual_friends, 
        friendship_duration: thresholds.connection.friendship_duration,
        total_friends: thresholds.user.total_friends,
        age_of_account: thresholds.user.age_of_account,
        minimum_trust_value:thresholds.minimum_trust_value,
        selected_action:thresholds.selected_action
    });

    const { mutual_friends, friendship_duration, total_friends, age_of_account, minimum_trust_value, selected_action } = formData;

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = e => {
        e.preventDefault();
        create_filtered_graph(user,formData)
    };

    return (
        <>
         <br/>
         <br/>
        <form className="row g-3" onSubmit={e => onSubmit(e)}>
            <CSRFToken/>
            <div className="col-12">
            <label className='form-label' for="minimum_trust_value">
                    <h3>
                    The Minimum Trust Value: {minimum_trust_value} 
                    </h3>
                </label>
                <br/>
                <input 
                type="range" 
                className="form-range" 
                min="0" 
                max="1" 
                step="0.05"
                defaultValue={minimum_trust_value}
                value={minimum_trust_value} 
                name="minimum_trust_value"
                onChange={e => onChange(e)}
                id="customRange3"
                />
                <br/>
            </div>
            <div className="col-md-6">
                <label for="mutual_friends">Mutual Friends: </label>
                <input
                        className='form-control'
                        type='number'
                        placeholder={mutual_friends}
                        name='mutual_friends'
                        id='mutual_friends'
                        value={mutual_friends}
                        onChange={e => onChange(e)}
                        required
                />
            </div>
            <div className="col-md-6">
                <label for="friendship_duration">Friendship Duration: </label>
                <input
                        className='form-control'
                        type='number'
                        placeholder={friendship_duration}
                        name='friendship_duration'
                        id="friendship_duration"
                        value={friendship_duration}
                        onChange={e => onChange(e)}
                        required
                    />
                </div>
                <div className="col-md-6">
                <label for="total_friends">Total Friends: </label>
                <input
                        className='form-control'
                        type='number'
                        placeholder={total_friends}
                        name='total_friends'
                        id='total_friends'
                        value={total_friends}
                        onChange={e => onChange(e)}
                        required
                    />
                </div>
                <div className="col-md-6">
                <label for="age_of_account">Age Of Account: </label>
                <input
                        className='form-control'
                        type='number'
                        placeholder={age_of_account}
                        name='age_of_account'
                        id='age_of_account'
                        value={age_of_account}
                        onChange={e => onChange(e)}
                        required
                    />
                </div>
                <br/>
                <br/>
                <label for="selected_action">Select An Action: </label>
                <select 
                name="selected_action" 
                onChange={e =>onChange(e)}
                value={selected_action}
                class="form-select form-select-lg mb-3"
                aria-label=".form-select-lg example">
                {actions.map(action =><option label={action} value={action}>
                </option>)}
                </select>

                <button className='btn btn-primary' type='submit'>Filter Network</button>
            </form>
            </>
        )
}

const mapStateToProps = state => ({
    user:state.auth.user,
    thresholds: state.network.thresholds
});

export default connect(mapStateToProps,{create_filtered_graph})(NetworkFilters)