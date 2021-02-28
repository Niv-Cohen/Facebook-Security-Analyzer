import React, { useState } from 'react';
import { Link, Redirect } from 'react-router-dom';
import {connect} from 'react-redux';
import { login } from '../actions/auth';
import CSRFToken from '../components/CSRFToken'

const Login = ({ login, isAuthenticated }) => {
    const [formData, setFormData] = useState({
        email: '',
        password: '' 
    });

    const { email, password } = formData;

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = e => {
        e.preventDefault();
        login(email, password);

    };

    if (isAuthenticated) {
        console.log('authenticated')
        return <Redirect to='/'  />
    }

    return (
        <div className='container mt-5'>
            <h1>Sign In</h1>
            <hr className='my-4' />
            <form onSubmit={e => onSubmit(e)}>
                <CSRFToken />
                <div class="mb-3">
                <label for="email" class="form-label">Email address</label>
                    <input
                        className='form-control'
                        type='email'
                        placeholder='Email'
                        id='email'
                        name='email'
                        value={email}
                        onChange={e => onChange(e)}
                        required
                    />
                </div>
                <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                    <input
                        className='form-control'
                        type='password'
                        placeholder='Password'
                        name='password'
                        id='password'
                        value={password}
                        onChange={e => onChange(e)}
                        minLength='6'
                        required
                    />
                </div>
                <button className='btn btn-primary' type='submit'>Login</button>
            </form>
            <p className="fw-bolder">
                Don't have an account? <Link to='/signup'>Sign Up</Link>
            </p>
            <p className="fw-bolder">
                Forgot your Password? <Link to='/reset-password'>Reset Password</Link>
            </p>
        </div>
    );
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated,
    
});

export default connect(mapStateToProps,{login})(Login);