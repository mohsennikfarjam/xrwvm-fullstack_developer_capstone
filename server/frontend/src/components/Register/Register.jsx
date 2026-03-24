import React, { useState } from "react";
import "./Register.css";
import Header from '../Header/Header';

const Register = () => {
  const [userName, setUserName] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const register = async (e) => {
    e.preventDefault();
    let register_url = window.location.origin + "/djangoapp/register";
    
    const res = await fetch(register_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        "userName": userName,
        "password": password,
        "firstName": firstName,
        "lastName": lastName,
        "email": email
      }),
    });

    const json = await res.json();
    if (json.status === "Authenticated") {
      sessionStorage.setItem('username', json.userName);
      window.location.href = "/";
    } else {
      alert(json.error || "Registration failed");
    }
  };

  return (
    <div>
      <Header/>
      <div className="register_container">
        <div className="modalContainer">
          <form className="login_panel" onSubmit={register}>
            <div className="header_panel">
              <span className="title">Sign Up</span>
            </div>
            
            <div className="input_group">
              <span className="input_field">Username</span>
              <input type="text" name="username" placeholder="Username" className="input_field" onChange={(e) => setUserName(e.target.value)} required/>
            </div>
            
            <div className="input_group">
              <span className="input_field">First Name</span>
              <input type="text" name="firstname" placeholder="First Name" className="input_field" onChange={(e) => setFirstName(e.target.value)} required/>
            </div>

            <div className="input_group">
              <span className="input_field">Last Name</span>
              <input type="text" name="lastname" placeholder="Last Name" className="input_field" onChange={(e) => setLastName(e.target.value)} required/>
            </div>

            <div className="input_group">
              <span className="input_field">Email</span>
              <input type="email" name="email" placeholder="Email" className="input_field" onChange={(e) => setEmail(e.target.value)} required/>
            </div>

            <div className="input_group">
              <span className="input_field">Password</span>
              <input type="password" name="psw" placeholder="Password" className="input_field" onChange={(e) => setPassword(e.target.value)} required/>
            </div>

            <div className="action_panel">
              <input className="action_button" type="submit" value="Register"/>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Register;
