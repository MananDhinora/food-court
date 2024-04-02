import React from 'react'
import './Footer.css'
import { assets } from '../../assets/assets'

const Footer = () => {
    return (
        <div className='footer' id='footer'>
            <div className="footer-content">
                <div className="footer-content-left">
                    <div className="footer-logo">
                    <img src={assets.logo} alt="" />
                    </div>
                    
                    <p>At Silver Oak University Food Court we prefer to provide our students and faculties with food options that are healthy, homely, tastey yet inexpensive that benefits health and cravings of our academics. And in which we depict our care as an organisation.</p>
                    <div className="footer-social-icons">
                        <img src={assets.facebook_icon} alt="" />
                        <img src={assets.twitter_icon} alt="" />
                        <img src={assets.linkedin_icon} alt="" />
                    </div>

                </div>
                <div className="footer-content-center">
                    <h2>COMPANY</h2>
                    <ul>
                        <li>Home</li>
                        <li>About us</li>
                        <li>Delivery</li>
                        <li>Privacy policy</li>
                    </ul>
                </div>
                <div className="footer-content-right">
                    <h2>GET IN TOUCH</h2>
                    <ul>
                        <li>+91-79-66046300</li>
                        <li>+91 90990 63464</li>
                        <li>info@silveroakuni.ac.in</li>
                        <li>www.silveroakuni.ac.in</li>
                    </ul>
                </div>

            </div>
            <hr />
            <p className="footer-copyright">Copyright 2024 @ silveroakuni.ac.in - All Right Reserved</p>
        </div>
    )
}

export default Footer