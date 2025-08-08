import React from "react";

const SelectionSummary = ({ summary, onContinue }) => {
  const { total_count, category_counts } = summary;

  if (total_count === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6 text-center">
        <div className="text-gray-500">
          <svg className="w-12 h-12 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
          <p className="text-lg font-medium text-gray-700">Your cart is empty</p>
          <p className="text-gray-500 mt-1">Add some delicious dishes to get started!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white shadow-lg border-t p-4">
      <div className="max-w-4xl mx-auto">
        {/* Selection counts */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4 text-sm">
            {Object.entries(category_counts).map(([category, count]) => {
              if (count === 0) return null;
              const displayName = {
                STARTER: "Starter",
                MAIN_COURSE: "Main Course", 
                DESSERT: "Dessert",
                SIDES: "Sides"
              }[category];
              
              return (
                <div key={category} className="flex items-center gap-1">
                  <span className="font-medium text-gray-700">{displayName}:</span>
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium">
                    {count}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Total and Continue button */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-lg font-semibold text-gray-800">
              Total Items: 
            </span>
            <span className="bg-blue-500 text-white px-3 py-1 rounded-full font-bold">
              {total_count}
            </span>
          </div>
          
          <button
            onClick={onContinue}
            className="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors duration-200 flex items-center gap-2"
          >
            <span>Continue</span>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default SelectionSummary;