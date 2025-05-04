import React from 'react';
import { Routes, Route } from 'react-router-dom';

// Import your components
import LoginPanel from './components/Login/Login';  // Your Login component
import RegisterPanel from './components/Register/Register';  // Your Register component
import Header from './components/Header/Header';  // Your Home component
import Dealers from './components/Dealers/Dealers'; 
import Dealer from "./components/Dealers/Dealer";
import PostReview from "./components/Dealers/PostReview";

function App() {
  return (
    <Routes>
      {/* Header Route */}
      <Route path="/" element={<Header />} />
      
      {/* Login Page Route */}
      <Route path="/login" element={<LoginPanel />} />
      
      {/* Register Page Route */}
      <Route path="/register" element={<RegisterPanel />} />
      <Route path="/dealers" element={<Dealers/>} />
      <Route path="/dealer/:id" element={<Dealer/>} />
      <Route path="/postreview/:id" element={<PostReview/>} />
    </Routes>
  );
}

export default App;
