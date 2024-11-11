import React, { useState, useEffect } from 'react';
import Navbar from './Navbar';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faExpand, faDownload } from '@fortawesome/free-solid-svg-icons';

const Home = () => {
  const [images, setImages] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);

  useEffect(() => {
    // Mock data for testing the UI
    const mockImages = [
      {
        title: 'Plot 1',
        src: 'https://via.placeholder.com/300?text=Plot+1',
      },
      {
        title: 'Plot 2',
        src: 'https://via.placeholder.com/300?text=Plot+2',
      },
      {
        title: 'Plot 3',
        src: 'https://via.placeholder.com/300?text=Plot+3',
      },
      {
        title: 'Plot 4',
        src: 'https://via.placeholder.com/300?text=Plot+3',
      },
      {
        title: 'Plot 5',
        src: 'https://via.placeholder.com/300?text=Plot+3',
      },
      {
        title: 'Plot 6',
        src: 'https://via.placeholder.com/300?text=Plot+3',
      },
      {
        title: 'Plot 7',
        src: 'https://via.placeholder.com/300?text=Plot+3',
      },
      {
        title: 'Plot 8',
        src: 'https://via.placeholder.com/300?text=Plot+3',
      },
      {
        title: 'Plot 9',
        src: 'https://via.placeholder.com/300?text=Plot+3',
      },
      {
        title: 'Plot 10',
        src: 'https://via.placeholder.com/300?text=Plot+3',
      },
      // Add more mock images as needed
    ];

    setImages(mockImages);
  }, []);

  const handleViewImage = (image) => {
    setSelectedImage(image);
  };

  const handleDownloadImage = (image) => {
    const link = document.createElement('a');
    link.href = image.src;
    link.download = image.title;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div>
      <Navbar />
      <div className="flex flex-col items-center justify-center min-h-screen pt-16">
        <h1 className="text-3xl font-bold mb-8 mt-8 text-center">Advertisement Response Analysis</h1>
        <div className="flex flex-wrap justify-center gap-8 w-full px-4">
          {images.map((image, index) => (
            <div key={index} className="border p-6 rounded-lg shadow-lg w-full md:w-1/3 lg:w-1/4 flex flex-col items-center">
              <h2 className="text-xl font-semibold mb-4 text-center">{image.title}</h2>
              <img src={image.src} alt={image.title} className="mb-4 rounded-lg" />
              <div className="flex justify-between w-full">
                <button
                  className="bg-blue-500 text-white px-4 py-2 rounded flex items-center mr-2 justify-center w-1/2 text-xs"
                  onClick={() => handleViewImage(image)}
                >
                  <FontAwesomeIcon icon={faExpand} className="mr-2" />
                  View Full Page
                </button>
                <button
                  className="bg-green-500 text-white px-4 py-2 rounded flex items-center ml-2 justify-center w-1/2 text-xs"
                  onClick={() => handleDownloadImage(image)}
                >
                  <FontAwesomeIcon icon={faDownload} className="mr-2" />
                  Download
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {selectedImage && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center">
          <div className="relative">
            <button
              className="absolute top-0 right-0 bg-red-500 text-white px-4 py-2 rounded"
              onClick={() => setSelectedImage(null)}
            >
              Close
            </button>
            <img src={selectedImage.src} alt={selectedImage.title} className="rounded-lg" />
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;