import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const IngredientScreen = () => {
  const { dishId } = useParams();
  const navigate = useNavigate();
  const [dishWithIngredients, setDishWithIngredients] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDishIngredients = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`${API}/dishes/${dishId}/ingredients`);
        setDishWithIngredients(response.data);
      } catch (err) {
        console.error("Error fetching ingredients:", err);
        setError("Failed to load dish ingredients");
      } finally {
        setLoading(false);
      }
    };

    if (dishId) {
      fetchDishIngredients();
    }
  }, [dishId]);

  const getVegIcon = (type) => {
    return type === "VEG" ? (
      <div className="w-5 h-5 border-2 border-green-500 flex items-center justify-center">
        <div className="w-2.5 h-2.5 bg-green-500 rounded-full"></div>
      </div>
    ) : (
      <div className="w-5 h-5 border-2 border-red-500 flex items-center justify-center">
        <div className="w-2.5 h-2.5 bg-red-500 rounded-full"></div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading ingredients...</p>
        </div>
      </div>
    );
  }

  if (error || !dishWithIngredients) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-xl mb-4">⚠️</div>
          <p className="text-gray-600 mb-4">{error || "Dish not found"}</p>
          <button
            onClick={() => navigate("/")}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
          >
            Back to Menu
          </button>
        </div>
      </div>
    );
  }

  const { dish, ingredients } = dishWithIngredients;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto p-4">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate("/")}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
            </button>
            <h1 className="text-2xl font-bold text-gray-800">Ingredients</h1>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto p-4">
        {/* Dish Info */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex flex-col md:flex-row gap-6">
            {/* Image */}
            <div className="md:w-1/3">
              <img
                src={dish.image || "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400"}
                alt={dish.name}
                className="w-full h-64 md:h-48 object-cover rounded-lg"
                onError={(e) => {
                  e.target.src = "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400";
                }}
              />
            </div>

            {/* Details */}
            <div className="md:w-2/3">
              <div className="flex items-start gap-3 mb-3">
                <h2 className="text-3xl font-bold text-gray-800 flex-1">
                  {dish.name}
                </h2>
                {getVegIcon(dish.type)}
              </div>
              
              <p className="text-gray-600 text-lg mb-4">
                {dish.description}
              </p>
              
              <div className="flex items-center gap-4 text-sm">
                <div className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full font-medium">
                  {dish.category.name}
                </div>
                <div className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full font-medium">
                  {dish.dishType}
                </div>
                <div className={`px-3 py-1 rounded-full font-medium ${
                  dish.type === "VEG" 
                    ? "bg-green-100 text-green-800" 
                    : "bg-red-100 text-red-800"
                }`}>
                  {dish.type === "VEG" ? "Vegetarian" : "Non-Vegetarian"}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Ingredients */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
            <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
            </svg>
            Ingredients & Quantities
          </h3>

          {ingredients.length === 0 ? (
            <div className="text-center py-8">
              <div className="text-gray-400 text-lg">No ingredients information available</div>
              <p className="text-gray-500 mt-2">We'll add detailed ingredients list soon!</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {ingredients.map((ingredient, index) => (
                <div 
                  key={index}
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    <span className="font-medium text-gray-800">
                      {ingredient.name}
                    </span>
                  </div>
                  <div className="text-blue-600 font-semibold">
                    {ingredient.quantity} {ingredient.unit}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Bottom spacing for mobile */}
        <div className="h-20"></div>
      </div>
    </div>
  );
};

export default IngredientScreen;