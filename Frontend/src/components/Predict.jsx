import React, { useState, useEffect } from 'react';
import Navbar from './Navbar';

const Predict = () => {
  const [inputs, setInputs] = useState({});
  const [dropdownOptions, setDropdownOptions] = useState({AdTopic: ['Education', 'Health']});
  const [prediction, setPrediction] = useState('');

  useEffect(() => {
    const fetchDropdownOptions = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/predict');
        const data = await response.json();
        // setDropdownOptions(data);
      } catch (error) {
        console.error('Error fetching dropdown options:', error);
      }
    };

    fetchDropdownOptions();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setInputs((prevInputs) => ({
      ...prevInputs,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log(inputs);
      const response = await fetch('http://localhost:8000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ model_inputs: inputs }),
      });
      const data = await response.json();
      setPrediction(`Predicted CTR: ${data.ctr}%, Conversion Rate: ${data.conversionRate}%`);
    } catch (error) {
      console.error('Error fetching prediction:', error);
    }
  };

  return (
    <div>
      <Navbar />
      <div className="flex flex-col md:flex-row gap-8 px-8 md:px-6 w-screen">
        <div className="flex flex-col items-center justify-center min-h-screen pt-16 w-full px-4">
          <h1 className="text-3xl font-bold mb-4">Predict CTR and Conversion Rate</h1>
          <form onSubmit={handleSubmit} className="mb-4 w-full max-w-md">
            <input
              type="text"
              name="Model"
              value={inputs.Model || 'Model1'}
              className="border p-2 rounded w-full mb-2"
              placeholder="Prediction Type 1"
            />
            <input
              type="number"
              name="AdCost"
              value={inputs.AdCost || ''}
              onChange={handleChange}
              className="border p-2 rounded w-full mb-2"
              placeholder="Ad Cost"
            />
            <input
              type="number"
              name="PurchaseAmount"
              value={inputs.PurchaseAmount || ''}
              onChange={handleChange}
              className="border p-2 rounded w-full mb-2"
              placeholder="Purchase Amount"
            />
            <select
              name="AdPlatformName"
              value={inputs.AdPlatformName || ''}
              onChange={handleChange}
              className="border p-2 rounded w-full mb-2"
            >
              <option value="">Select Ad Platform Name</option>
              {dropdownOptions.AdPlatformName?.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
            <select
              name="AdPlatformType"
              value={inputs.AdPlatformType || ''}
              onChange={handleChange}
              className="border p-2 rounded w-full mb-2"
            >
              <option value="">Select Ad Platform Type</option>
              {dropdownOptions.AdPlatformType?.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
            <select
              name="AdType"
              value={inputs.AdType || ''}
              onChange={handleChange}
              className="border p-2 rounded w-full mb-2"
            >
              <option value="">Select Ad Type</option>
              {dropdownOptions.AdType?.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
            <select
              name="AdTopic"
              value={inputs.AdTopic || ''}
              onChange={handleChange}
              className="border p-2 rounded w-full mb-2"
            >
              <option value="">Select Ad Topic</option>
              {dropdownOptions.AdTopic?.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
            <button type="submit" className="bg-blue-500 text-white p-2 rounded w-full">Get Prediction</button>
          </form>
          {prediction && <p className="text-xl font-bold">{prediction}</p>}
        </div>
        <div className="flex flex-col items-center justify-center min-h-screen pt-16 w-full">
          <h1 className="text-3xl font-bold mb-4">Predict Recommended Ad Topic</h1>
          <form onSubmit={handleSubmit} className="mb-4 w-full max-w-md">
            <input
              type="text"
              name="Model"
              value={inputs.Model || 'Model2'}
              className="border p-2 rounded w-full mb-2"
              placeholder="Prediction Type 2"
            />
            <select
              name="Age"
              value={inputs.Age || ''}
              onChange={handleChange}
              className="border p-2 rounded w-full mb-2"
            >
              <option value="">Select Age</option>
              {dropdownOptions.Age?.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
            <select
              name="Gender"
              value={inputs.Gender || ''}
              onChange={handleChange}
              className="border p-2 rounded w-full mb-2"
            >
              <option value="">Select Gender</option>
              {dropdownOptions.Gender?.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
            <select
              name="Location"
              value={inputs.Location || ''}
              onChange={handleChange}
              className="border p-2 rounded w-full mb-2"
            >
              <option value="">Select Location</option>
              {dropdownOptions.Location?.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
            <select
              name="Income_Level"
              value={inputs.Income_Level || ''}
              onChange={handleChange}
              className="border p-2 rounded w-full mb-2"
            >
              <option value="">Select Income Level</option>
              {dropdownOptions.Income_Level?.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
            <select
              name="Education_Level"
              value={inputs.Education_Level || ''}
              onChange={handleChange}
              className="border p-2 rounded w-full mb-2"
            >
              <option value="">Select Education Level</option>
              {dropdownOptions.Education_Level?.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
            <select
              name="Occupation"
              value={inputs.Occupation || ''}
              onChange={handleChange}
              className="border p-2 rounded w-full mb-2"
            >
              <option value="">Select Occupation</option>
              {dropdownOptions.Occupation?.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
            <button type="submit" className="bg-blue-500 text-white p-2 rounded w-full">Get Prediction</button>
          </form>
          {prediction && <p className="text-xl font-bold">{prediction}</p>}
        </div>
      </div>
    </div>
  );
};

export default Predict;