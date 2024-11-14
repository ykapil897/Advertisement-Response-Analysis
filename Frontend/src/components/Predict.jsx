import React, { useState } from 'react';
import Navbar from './Navbar';

const Predict = () => {
  const [input, setInput] = useState('');
  const [prediction, setPrediction] = useState(null);

  const handlePredict = () => {
    // Call your backend API to get the prediction
    // For now, we'll just set a dummy prediction
    setPrediction('Predicted CTR: 15%, Conversion Rate: 5%');
  };

  return (
    <div>
      <Navbar />
      <div className="flex flex-col items-center justify-center min-h-screen pt-16 w-screen">
        <h1 className="text-3xl font-bold mb-4">Predict CTR and Conversion Rate</h1>
        <div className="mb-4 w-full max-w-md">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="border p-2 rounded w-full"
            placeholder="Enter input for prediction"
          />
        </div>
        <button onClick={handlePredict} className="bg-blue-500 text-white px-4 py-2 rounded">Predict</button>
        {prediction && <p className="mt-4">{prediction}</p>}
      </div>
    </div>
  );
};

export default Predict;