import React from 'react';
import Navbar from './Navbar';

const Analyse = () => {
  return (
    <div>
      <Navbar />
      <div className="flex flex-col items-center justify-center min-h-screen pt-16">
        <h1 className="text-3xl font-bold mb-4">Analyse Data</h1>
        <p>Select attributes to display charts and graphs.</p>
        {/* Add your chart components and logic here */}
      </div>
    </div>
  );
};

export default Analyse;