import React from "react";

const FilterToggle = ({ vegFilter, nonVegFilter, onVegToggle, onNonVegToggle }) => {
  return (
    <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
      <div className="flex items-center justify-center gap-6">
        <label className="flex items-center gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={vegFilter}
            onChange={(e) => onVegToggle(e.target.checked)}
            className="sr-only"
          />
          <div className={`w-12 h-6 rounded-full transition-all duration-200 relative ${
            vegFilter ? "bg-green-500" : "bg-gray-300"
          }`}>
            <div className={`w-5 h-5 bg-white rounded-full absolute top-0.5 transition-transform duration-200 ${
              vegFilter ? "translate-x-6" : "translate-x-0.5"
            }`}></div>
          </div>
          <span className="flex items-center gap-2">
            <div className="w-4 h-4 border-2 border-green-500 flex items-center justify-center">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            </div>
            <span className="font-medium text-gray-700">Veg</span>
          </span>
        </label>

        <label className="flex items-center gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={nonVegFilter}
            onChange={(e) => onNonVegToggle(e.target.checked)}
            className="sr-only"
          />
          <div className={`w-12 h-6 rounded-full transition-all duration-200 relative ${
            nonVegFilter ? "bg-red-500" : "bg-gray-300"
          }`}>
            <div className={`w-5 h-5 bg-white rounded-full absolute top-0.5 transition-transform duration-200 ${
              nonVegFilter ? "translate-x-6" : "translate-x-0.5"
            }`}></div>
          </div>
          <span className="flex items-center gap-2">
            <div className="w-4 h-4 border-2 border-red-500 flex items-center justify-center">
              <div className="w-2 h-2 bg-red-500 rounded-full"></div>
            </div>
            <span className="font-medium text-gray-700">Non-Veg</span>
          </span>
        </label>
      </div>
    </div>
  );
};

export default FilterToggle;