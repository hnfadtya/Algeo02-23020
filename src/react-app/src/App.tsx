import ListGroup from "./components/ListGroup";
import Header from "./components/Header";
import React from 'react';
import './App.css';
import Navbar from "./components/Navbar";
import Body from "./components/Body";

function App(){
  return (
  <div className="mainBackground">
    <Navbar/>
    <Header/>
    <Body/>
  </div>
  
  );
}

export default App;