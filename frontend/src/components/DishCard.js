import React from "react";
import { useNavigate } from "react-router-dom";

const DishCard = ({ dish, isSelected, selectedQuantity, onAdd, onRemove }) => {
  const navigate = useNavigate();

  const handleIngredientsClick = () => {
    navigate(`/ingredients/${dish.id}`);
  };

  const getVegIcon = () => {
    return dish.type === "VEG" ? (
      <div className="w-4 h-4 border-2 border-green-500 flex items-center justify-center">
        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
      </div>
    ) : (
      <div className="w-4 h-4 border-2 border-red-500 flex items-center justify-center">
        <div className="w-2 h-2 bg-red-500 rounded-full"></div>
      </div>
    );
  };

  return (
    <div className={`bg-white rounded-lg shadow-sm border-2 transition-all duration-200 hover:shadow-md ${
      isSelected ? "border-blue-500 bg-blue-50" : "border-gray-100"
    }`}>
      {/* Image */}
      <div className="relative">
        <img
          src={dish.image || "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400"}
          alt={dish.name}
          className="w-full h-48 object-cover rounded-t-lg"
          onError={(e) => {
            e.target.src = "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400";
          }}
        />
        {isSelected && (
          <div className="absolute top-2 right-2 bg-blue-500 text-white px-2 py-1 rounded-full text-sm font-medium">
            Added ({selectedQuantity})
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-4">
        {/* Name and Veg Indicator */}
        <div className="flex items-start justify-between mb-2">
          <h3 className="font-semibold text-gray-800 text-lg leading-tight flex-1">
            {dish.name}
          </h3>
          <div className="ml-2 mt-1">
            {getVegIcon()}
          </div>
        </div>

        {/* Description */}
        <p className="text-gray-600 text-sm mb-3 line-clamp-2">
          {dish.description}
        </p>

        {/* Category */}
        <div className="text-xs text-gray-500 mb-3">
          {dish.category.name} • {dish.dishType}
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-between gap-2">
          <button
            onClick={handleIngredientsClick}
            className="text-blue-500 text-sm font-medium hover:text-blue-600 underline"
          >
            Ingredients
          </button>
          
          <div className="flex items-center gap-2">
            {isSelected ? (
              <button
                onClick={onRemove}
                className="px-4 py-2 bg-red-500 text-white text-sm font-medium rounded-lg hover:bg-red-600 transition-colors"
              >
                Remove
              </button>
            ) : (
              <button
                onClick={onAdd}
                className="px-4 py-2 bg-blue-500 text-white text-sm font-medium rounded-lg hover:bg-blue-600 transition-colors"
              >
                Add
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DishCard;