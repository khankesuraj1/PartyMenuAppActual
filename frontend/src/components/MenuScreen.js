import React, { useState, useEffect } from "react";
import axios from "axios";
import DishCard from "./DishCard";
import SearchBar from "./SearchBar";
import FilterToggle from "./FilterToggle";
import SelectionSummary from "./SelectionSummary";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const MEAL_TYPES = [
  { key: "STARTER", label: "Starter" },
  { key: "MAIN_COURSE", label: "Main Course" },
  { key: "DESSERT", label: "Dessert" },
  { key: "SIDES", label: "Sides" }
];

const MenuScreen = () => {
  const [dishes, setDishes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedMealType, setSelectedMealType] = useState("STARTER");
  const [searchQuery, setSearchQuery] = useState("");
  const [vegFilter, setVegFilter] = useState(true);
  const [nonVegFilter, setNonVegFilter] = useState(true);
  const [selections, setSelections] = useState({});
  const [selectionSummary, setSelectionSummary] = useState({
    total_count: 0,
    category_counts: { STARTER: 0, MAIN_COURSE: 0, DESSERT: 0, SIDES: 0 }
  });

  const userId = "user123"; // In real app, this would come from authentication

  // Fetch dishes based on current filters
  const fetchDishes = async () => {
    setLoading(true);
    try {
      let url = `${API}/dishes?meal_type=${selectedMealType}`;
      
      if (searchQuery) {
        url += `&search=${encodeURIComponent(searchQuery)}`;
      }

      const response = await axios.get(url);
      let filteredDishes = response.data;

      // Apply veg/non-veg filter on frontend since API doesn't handle both
      if (!vegFilter && !nonVegFilter) {
        filteredDishes = [];
      } else if (!vegFilter) {
        filteredDishes = filteredDishes.filter(dish => dish.type === "NON_VEG");
      } else if (!nonVegFilter) {
        filteredDishes = filteredDishes.filter(dish => dish.type === "VEG");
      }

      setDishes(filteredDishes);
    } catch (error) {
      console.error("Error fetching dishes:", error);
    } finally {
      setLoading(false);
    }
  };

  // Fetch selection summary
  const fetchSelectionSummary = async () => {
    try {
      const response = await axios.get(`${API}/selections/${userId}`);
      setSelectionSummary(response.data);
      
      // Convert selections array to object for easy lookup
      const selectionsObj = {};
      response.data.selections.forEach(sel => {
        selectionsObj[sel.dish_id] = sel.quantity;
      });
      setSelections(selectionsObj);
    } catch (error) {
      console.error("Error fetching selections:", error);
    }
  };

  useEffect(() => {
    fetchDishes();
  }, [selectedMealType, searchQuery, vegFilter, nonVegFilter]);

  useEffect(() => {
    fetchSelectionSummary();
  }, []);

  const handleAddDish = async (dishId) => {
    try {
      await axios.post(`${API}/selections/${userId}`, {
        dish_id: dishId,
        quantity: 1
      });
      await fetchSelectionSummary();
    } catch (error) {
      console.error("Error adding dish:", error);
    }
  };

  const handleRemoveDish = async (dishId) => {
    try {
      await axios.delete(`${API}/selections/${userId}/${dishId}`);
      await fetchSelectionSummary();
    } catch (error) {
      console.error("Error removing dish:", error);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
        <h1 className="text-3xl font-bold text-gray-800 text-center mb-2">
          Party Menu Selection
        </h1>
        <p className="text-gray-600 text-center">
          Choose delicious dishes for your party
        </p>
      </div>

      {/* Search Bar */}
      <SearchBar 
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
      />

      {/* Filters */}
      <FilterToggle 
        vegFilter={vegFilter}
        nonVegFilter={nonVegFilter}
        onVegToggle={setVegFilter}
        onNonVegToggle={setNonVegFilter}
      />

      {/* Category Tabs */}
      <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
        <div className="flex flex-wrap gap-2">
          {MEAL_TYPES.map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setSelectedMealType(key)}
              className={`px-4 py-2 rounded-full font-medium transition-all duration-200 flex items-center gap-2 ${
                selectedMealType === key
                  ? "bg-blue-500 text-white shadow-lg"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              {label}
              {selectionSummary.category_counts[key] > 0 && (
                <span className={`text-xs px-2 py-1 rounded-full ${
                  selectedMealType === key 
                    ? "bg-white text-blue-500"
                    : "bg-blue-500 text-white"
                }`}>
                  {selectionSummary.category_counts[key]}
                </span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Dishes Grid */}
      <div className="mb-6">
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          </div>
        ) : dishes.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-gray-400 text-lg">No dishes found</div>
            <p className="text-gray-500 mt-2">Try adjusting your search or filters</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {dishes.map(dish => (
              <DishCard
                key={dish.id}
                dish={dish}
                isSelected={!!selections[dish.id]}
                selectedQuantity={selections[dish.id] || 0}
                onAdd={() => handleAddDish(dish.id)}
                onRemove={() => handleRemoveDish(dish.id)}
              />
            ))}
          </div>
        )}
      </div>

      {/* Selection Summary */}
      <SelectionSummary 
        summary={selectionSummary}
        onContinue={() => alert("Proceeding with your selection!")}
      />
    </div>
  );
};

export default MenuScreen;