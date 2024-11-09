import React from 'react';
import { Link } from 'react-router-dom';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import Navbar from './Navbar';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const Home = () => {
  const data = {
    labels: ['Ad 1', 'Ad 2', 'Ad 3', 'Ad 4'],
    datasets: [
      {
        label: 'Click Through Rate',
        data: [12, 19, 3, 5],
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      },
      {
        label: 'Conversion Rate',
        data: [2, 3, 20, 5],
        backgroundColor: 'rgba(153, 102, 255, 0.6)',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Advertisement Performance',
      },
    },
  };

  return (
    <div>
      <Navbar />
      <div className="flex flex-col items-center justify-center min-h-screen pt-16">
        <h1 className="text-3xl font-bold mb-4">Advertisement Response Analysis</h1>
        <div className="mb-4 w-full max-w-4xl">
          <Bar data={data} options={options} />
        </div>
      </div>
    </div>
  );
};

export default Home;