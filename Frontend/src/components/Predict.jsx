import React, { useState, useEffect } from 'react';
import Navbar from './Navbar';

const Predict = () => {
  const [model1_inputs, setInputs1] = useState({Model: 'Model1'});
  const [model2_inputs, setInputs2] = useState({Model: 'Model2'});
  const [dropdownOptions, setDropdownOptions] = useState({});
  const [prediction1, setPrediction1] = useState('');
  const [prediction2, setPrediction2] = useState('');

  useEffect(() => {
    const fetchDropdownOptions = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/predict/');
        const data = await response.json();
        setDropdownOptions(data);
      } catch (error) {
        console.error('Error fetching dropdown options:', error);
      }
    };

    fetchDropdownOptions();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setInputs1((prevInputs) => ({
      ...prevInputs,
      [name]: value,
    }));
    setInputs2((prevInputs) => ({
      ...prevInputs,
      [name]: value,
    }));
  };

  const handleSubmit1 = async (e) => {
    e.preventDefault();
    try {
      console.log(model1_inputs);
      const response = await fetch('http://localhost:8000/api/predict/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ model_inputs: model1_inputs }),
      });
      const data = await response.json();
      // console.log(data, data[0], data[0]);
      setPrediction1(`CTR: ${data[0]}\n Conversion Rate: ${data[1]}`);
    } catch (error) {
      console.error('Error fetching prediction1:', error);
    }
  };

  const handleSubmit2 = async (e) => {
    e.preventDefault();
    try {
      console.log(model2_inputs);
      const response = await fetch('http://localhost:8000/api/predict/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ model_inputs: model2_inputs }),
      });
      const data = await response.json();
      console.log(data);
      setPrediction2(`Predicted Ad Topic: ${data.predicted_topics[0]}`);
    } catch (error) {
      console.error('Error fetching prediction1:', error);
    }
  };

  return (
    <div>
      <Navbar />
      <div className="flex flex-col md:flex-row gap-8 px-8 md:px-6 w-screen">
        <div className="flex flex-col items-center justify-center min-h-screen pt-16 w-full px-4">
          <h1 className="text-3xl font-bold mb-4">Predict CTR and Conversion Rate</h1>
          <form onSubmit={handleSubmit1} className="mb-4 w-full max-w-md">
            <input
              type="text"
              name="Model"
              value={model1_inputs.Model || 'Model1'}
              className="border p-2 rounded w-full mb-2"
              placeholder="Prediction Type 1"
            />
            <input
              type="number"
              name="AdCost"
              value={model1_inputs.AdCost || ''}
              onChange={handleChange}
              className="border p-2 rounded w-full mb-2"
              placeholder="Ad Cost"
            />
            <input
              type="number"
              name="PurchaseAmount"
              value={model1_inputs.PurchaseAmount || ''}
              onChange={handleChange}
              className="border p-2 rounded w-full mb-2"
              placeholder="Purchase Amount"
            />
            <select
              name="AdPlatformName"
              value={model1_inputs.AdPlatformName || ''}
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
              value={model1_inputs.AdPlatformType || ''}
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
              value={model1_inputs.AdType || ''}
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
              value={model1_inputs.AdTopic || ''}
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
          {prediction1 && (
            <p className="text-xl font-bold text-wrap" style={{ whiteSpace: 'pre' }}>
              {prediction1}
            </p>
          )}
        </div>
        <div className="flex flex-col items-center justify-center min-h-screen pt-16 w-full">
          <h1 className="text-3xl font-bold mb-4">Predict Recommended Ad Topic</h1>
          <form onSubmit={handleSubmit2} className="mb-4 w-full max-w-md">
            <input
              type="text"
              name="Model"
              value={model2_inputs.Model || 'Model2'}
              className="border p-2 rounded w-full mb-2"
              placeholder="Prediction Type 2"
            />
            <select
              name="Age"
              value={model2_inputs.Age || ''}
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
              name="Education Level"
              value={model2_inputs.Education_Level || ''}
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
              name="Gender"
              value={model2_inputs.Gender || ''}
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
              name="Income Level"
              value={model2_inputs.Income_Level || ''}
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
              name="Location"
              value={model2_inputs.Location || ''}
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
              name="Occupation"
              value={model2_inputs.Occupation || ''}
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
          {prediction2 && <p className="text-xl font-bold">{prediction2}</p>}
        </div>
      </div>
    </div>
  );
};

export default Predict;