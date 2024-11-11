// src/components/Navbar.jsx
import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-gray-800 p-4 w-full fixed top-0 left-0 z-10">
      <div className="container mx-auto flex justify-center">
        <div className="flex space-x-4">
          <Link to="/" className="text-white px-3 py-2 rounded-md text-sm font-medium">Home</Link>
          <Link to="/analyse" className="text-white px-3 py-2 rounded-md text-sm font-medium">Analyse</Link>
          <Link to="/predict" className="text-white px-3 py-2 rounded-md text-sm font-medium">Predict</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;