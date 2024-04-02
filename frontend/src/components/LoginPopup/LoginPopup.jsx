import React, { useState } from 'react'
import './LoginPopup.css'
import { assets } from '../../assets/assets'

const LoginPopup = ({ setShowLogin }) => {

    const [currState, setCurrState] = useState("Login");

    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [userType, setUserType] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    const handleSubmit = async () => {
        setErrorMessage('');
        setSuccessMessage('');

        if (currState === 'Login') {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password }),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    setErrorMessage(errorData.error);
                    return;
                }

                setSuccessMessage('User login success!');
                setEmail('');
                setPassword('');
            } catch (error) {
                console.error('Error during login:', error);
                setErrorMessage('An error occurred. Please try again.');
            }
        }
        else {
            console.log(name, email, password, userType);
            try {
                const response = await fetch('http://127.0.0.1:5000/api/signup', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email, password, userType }),
                });
                console.log(response)

                if (!response.ok) {
                    const errorData = await response.json();
                    setErrorMessage(errorData.error);
                    return;
                }

                setSuccessMessage('User Signup success!');
                setName('');
                setEmail('');
                setPassword('');
                setUserType('');
            } catch (error) {
                console.error('Error during signup:', error);
                setErrorMessage('An error occurred. Please try again.');
            }
        }

    };

    return (
        <div className='login-popup'>
            <form className="login-popup-container" onSubmit={handleSubmit}>
                <div className="login-popup-title">
                    <h2>{currState}</h2>
                    {errorMessage && <p className="error-message">{errorMessage}</p>}
                    {successMessage && <p className="success-message">{successMessage}</p>}
                    <img onClick={() => setShowLogin(false)} src={assets.cross_icon} alt="" />
                </div>
                <div className="login-popup-inputs">
                    {currState === "Login" ? <></> : <input type="text" placeholder='Your name' id='name' value={name} onChange={(e) => setName(e.target.value)} required />}
                    <input type="email" placeholder='Your email' id='email' value={email} onChange={(e) => setEmail(e.target.value)} required />
                    <input type="password" placeholder='Password' id='password' value={password} onChange={(e) => setPassword(e.target.value)} required />
                    {currState === "Login" ? <></> : <select name="userType" placeholder="user-type" id='userType' value={userType} onChange={(e) => setUserType(e.target.value)} >
                        <option value='Student'>Student</option>
                        <option value='Faculty'>Faculty</option>
                    </select>}
                </div>
                <button>{currState === "Sign Up" ? "Create account" : "Login"}</button>
                <div className="login-popup-condition">
                    <input type="checkbox" required />
                    <p>By continuing, I agree to the terms of use & privacy policy.</p>
                </div>
                {currState === "Login"
                    ? <p>Create a new account? <span onClick={() => setCurrState("Sign Up")}>Click here</span></p>
                    : <p>Already have an account? <span onClick={() => setCurrState("Login")}>Login here</span></p>
                }
            </form>
        </div>
    )
}

export default LoginPopup