import { Feather, Ionicons, MaterialCommunityIcons } from "@expo/vector-icons";
import React, { useState } from "react";
import {
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";

import { QUERY_API_URL } from "../constants/api";

const API_URL = "http://localhost:5000";

export default function HomeScreen() {
  const [city, setCity] = useState("");
  const [loading, setLoading] = useState(false);

  const [weather, setWeather] = useState({
    city: "New Delhi",
    temperature: 28,
    condition: "Partly Cloudy",
    humidity: 72,
    wind: 14,
    feelsLike: 30,
  });

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState<
    { sender: "ai" | "user"; text: string }[]
  >([
    {
      sender: "ai",
      text: "Ask me anything about today's forecast, travel advisories, or planning your day.",
    },
  ]);

  // --------------------------------------------------
  // CITY WEATHER SEARCH
  // --------------------------------------------------

  const searchWeather = async () => {
    if (!city.trim()) return;

    setLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/api/weather?city=${encodeURIComponent(city.trim())}`
      );

      if (!response.ok) {
        throw new Error("Weather API error");
      }

      const data = await response.json();

      setWeather({
        city: data.city || city,
        temperature: data.temperature ?? 28,
        condition: data.condition || "Partly Cloudy",
        humidity: data.humidity ?? 72,
        wind: data.wind_speed ?? 14,
        feelsLike: data.feels_like ?? 30,
      });
    } catch (error) {
      console.error("WEATHER SEARCH ERROR:", error);
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------------------------
  // WEATHERGPT AI CHAT
  // --------------------------------------------------

  const askWeatherGPT = async () => {
    if (!question.trim()) return;

    const userQuestion = question.trim();

    // Show user's message immediately
    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: userQuestion,
      },
    ]);

    setQuestion("");

    try {
      const response = await fetch(QUERY_API_URL, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          message: userQuestion,

          // Temporary test location
          latitude: 28.5355,
          longitude: 77.391,
        }),
      });

      console.log("QUERY STATUS:", response.status);

      if (!response.ok) {
        throw new Error("Chat API error");
      }

      const data = await response.json();

      console.log("QUERY RESPONSE:", data);

      const recommendation = data.recommendation;

      let aiText =
        data.explanation ||
        "I couldn't analyze the forecast for your request.";

      // If Decision Engine produced a recommendation
      if (recommendation) {
        aiText =
          `${data.explanation || ""}\n\n` +
          `🌱 Best time: ${recommendation.best_time}\n` +
          `📊 Suitability: ${recommendation.score}/100\n` +
          `⚠️ Risk: ${recommendation.risk}`;

        // Best window
        if (recommendation.best_window) {
          aiText +=
            `\n⏰ Best window: ` +
            `${recommendation.best_window.start} - ` +
            `${recommendation.best_window.end}`;
        }
      }

      // Add AI response to chat
      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: aiText,
        },
      ]);
    } catch (error) {
      console.error("QUERY ERROR:", error);

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: "Sorry, I couldn't connect to the WeatherGPT backend.",
        },
      ]);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        style={{ flex: 1 }}
      >
        <ScrollView
          showsVerticalScrollIndicator={false}
          contentContainerStyle={styles.content}
          keyboardShouldPersistTaps="handled"
        >
          {/* HEADER */}
          <View style={styles.header}>
            <View>
              <Text style={styles.logo}>WeatherGPT</Text>

              <Text style={styles.subtitle}>
                Intelligent Forecast Assistant
              </Text>
            </View>

            <View style={styles.badgeContainer}>
              <Feather name="cpu" size={14} color="#60A5FA" />

              <Text style={styles.badgeText}>GPT-4o</Text>
            </View>
          </View>

          {/* SEARCH BAR */}
          <View style={styles.searchBox}>
            <Feather
              name="search"
              size={18}
              color="#64748B"
              style={styles.searchIcon}
            />

            <TextInput
              style={styles.searchInput}
              placeholder="Search city..."
              placeholderTextColor="#64748B"
              value={city}
              onChangeText={setCity}
              onSubmitEditing={searchWeather}
              returnKeyType="search"
            />

            <TouchableOpacity
              style={styles.searchButton}
              onPress={searchWeather}
              disabled={loading}
              activeOpacity={0.8}
            >
              {loading ? (
                <ActivityIndicator color="#FFFFFF" size="small" />
              ) : (
                <Text style={styles.searchButtonText}>Search</Text>
              )}
            </TouchableOpacity>
          </View>

          {/* CURRENT WEATHER HERO */}
          <View style={styles.weatherCard}>
            <View style={styles.weatherCardTop}>
              <View>
                <View style={styles.locationRow}>
                  <Ionicons
                    name="location-sharp"
                    size={14}
                    color="#60A5FA"
                  />

                  <Text style={styles.city}>{weather.city}</Text>
                </View>

                <Text style={styles.condition}>{weather.condition}</Text>
              </View>

              <Ionicons
                name="partly-sunny"
                size={54}
                color="#60A5FA"
              />
            </View>

            <View style={styles.weatherCardBottom}>
              <Text style={styles.temperature}>
                {weather.temperature}°
              </Text>

              <Text style={styles.feelsLikeText}>
                Feels like {weather.feelsLike}°
              </Text>
            </View>
          </View>

          {/* METRIC DETAILS */}
          <View style={styles.detailsRow}>
            <DetailCard
              icon={
                <Feather
                  name="droplet"
                  size={18}
                  color="#60A5FA"
                />
              }
              value={`${weather.humidity}%`}
              label="Humidity"
            />

            <DetailCard
              icon={
                <Feather
                  name="wind"
                  size={18}
                  color="#60A5FA"
                />
              }
              value={`${weather.wind} km/h`}
              label="Wind"
            />

            <DetailCard
              icon={
                <Feather
                  name="thermometer"
                  size={18}
                  color="#60A5FA"
                />
              }
              value={`${weather.feelsLike}°`}
              label="RealFeel"
            />
          </View>

          {/* 5-DAY FORECAST */}
          <Text style={styles.sectionTitle}>5-Day Forecast</Text>

          <View style={styles.forecastCard}>
            <ForecastItem
              day="Today"
              iconName="cloud"
              temp="28°"
              active
            />

            <ForecastItem
              day="Sat"
              iconName="partly-sunny"
              temp="30°"
            />

            <ForecastItem
              day="Sun"
              iconName="sunny"
              temp="31°"
            />

            <ForecastItem
              day="Mon"
              iconName="rainy"
              temp="27°"
            />

            <ForecastItem
              day="Tue"
              iconName="cloudy"
              temp="29°"
            />
          </View>

          {/* AI ADVISOR */}
          <View style={styles.sectionHeaderRow}>
            <Text style={styles.sectionTitle}>
              Weather Advisor
            </Text>

            <Text style={styles.sectionSubtitle}>
              AI-Powered
            </Text>
          </View>

          <View style={styles.chatCard}>
            {messages.map((message, index) => (
              <View
                key={index}
                style={
                  message.sender === "user"
                    ? styles.userMessage
                    : styles.aiMessage
                }
              >
                {message.sender === "ai" && (
                  <View style={styles.aiAvatar}>
                    <Ionicons
                      name="sparkles"
                      size={14}
                      color="#2563EB"
                    />
                  </View>
                )}

                <View
                  style={
                    message.sender === "user"
                      ? styles.userBubble
                      : styles.aiBubble
                  }
                >
                  <Text style={styles.messageText}>
                    {message.text}
                  </Text>
                </View>
              </View>
            ))}

            {/* CHAT INPUT */}
            <View style={styles.chatInputBox}>
              <TextInput
                style={styles.chatInput}
                placeholder="Ask advice (e.g., 'Will it rain during commute?')"
                placeholderTextColor="#64748B"
                value={question}
                onChangeText={setQuestion}
                onSubmitEditing={askWeatherGPT}
                returnKeyType="send"
              />

              <TouchableOpacity
                style={styles.sendButton}
                onPress={askWeatherGPT}
                activeOpacity={0.7}
              >
                <Feather
                  name="arrow-up"
                  size={18}
                  color="#FFFFFF"
                />
              </TouchableOpacity>
            </View>
          </View>

          {/* WEATHER ALERTS */}
          <Text style={styles.sectionTitle}>
            Advisories & Alerts
          </Text>

          <View style={styles.alertCard}>
            <View style={styles.alertIconWrapper}>
              <MaterialCommunityIcons
                name="shield-check-outline"
                size={22}
                color="#10B981"
              />
            </View>

            <View style={styles.alertContent}>
              <Text style={styles.alertTitle}>
                Standard Conditions
              </Text>

              <Text style={styles.alertText}>
                No severe storms, rain warnings, or wind advisories
                currently active in {weather.city}.
              </Text>
            </View>
          </View>

          {/* CLIMATE INFORMATION */}
          <Text style={styles.sectionTitle}>
            Climate Information
          </Text>

          <View style={styles.climateCard}>
            <View style={styles.climateHeader}>
              <Ionicons
                name="earth"
                size={20}
                color="#60A5FA"
              />

              <Text style={styles.climateTitle}>
                Understanding Regional Climate
              </Text>
            </View>

            <Text style={styles.climateText}>
              Explore long-term seasonal trends, historic rainfall
              patterns, and temperature anomalies in {weather.city}.
            </Text>

            <TouchableOpacity
              style={styles.exploreButton}
              activeOpacity={0.7}
            >
              <Text style={styles.exploreButtonText}>
                Explore Climate Data
              </Text>

              <Feather
                name="arrow-right"
                size={14}
                color="#60A5FA"
              />
            </TouchableOpacity>
          </View>

          {/* FOOTER */}
          <Text style={styles.footer}>
            WeatherGPT Engine • Version 1.0.0
          </Text>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

// --------------------------------------------------
// DETAIL CARD
// --------------------------------------------------

function DetailCard({
  icon,
  value,
  label,
}: {
  icon: React.ReactNode;
  value: string;
  label: string;
}) {
  return (
    <View style={styles.detailCard}>
      <View style={styles.iconContainer}>
        {icon}
      </View>

      <Text style={styles.detailValue}>
        {value}
      </Text>

      <Text style={styles.detailLabel}>
        {label}
      </Text>
    </View>
  );
}

// --------------------------------------------------
// FORECAST ITEM
// --------------------------------------------------

function ForecastItem({
  day,
  iconName,
  temp,
  active,
}: {
  day: string;
  iconName: any;
  temp: string;
  active?: boolean;
}) {
  return (
    <View
      style={[
        styles.forecastCol,
        active && styles.forecastColActive,
      ]}
    >
      <Text
        style={[
          styles.forecastDayText,
          active && styles.forecastDayActive,
        ]}
      >
        {day}
      </Text>

      <Ionicons
        name={iconName}
        size={22}
        color={active ? "#60A5FA" : "#94A3B8"}
        style={{ marginVertical: 8 }}
      />

      <Text style={styles.forecastTemp}>
        {temp}
      </Text>
    </View>
  );
}

// --------------------------------------------------
// STYLES
// --------------------------------------------------

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#0B132B",
  },

  content: {
    paddingHorizontal: 20,
    paddingTop: 12,
    paddingBottom: 130,
  },

  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 20,
  },

  logo: {
    fontSize: 26,
    fontWeight: "800",
    color: "#FFFFFF",
    letterSpacing: -0.5,
  },

  subtitle: {
    color: "#64748B",
    fontSize: 13,
    fontWeight: "500",
    marginTop: 2,
  },

  badgeContainer: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#1C2A4A",
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 20,
    gap: 5,
    borderWidth: 1,
    borderColor: "#253860",
  },

  badgeText: {
    color: "#93C5FD",
    fontWeight: "700",
    fontSize: 12,
  },

  searchBox: {
    height: 50,
    backgroundColor: "#16223F",
    borderRadius: 14,
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 12,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: "#23335A",
  },

  searchIcon: {
    marginRight: 8,
  },

  searchInput: {
    flex: 1,
    color: "#FFFFFF",
    fontSize: 15,
  },

  searchButton: {
    backgroundColor: "#2563EB",
    paddingVertical: 8,
    paddingHorizontal: 14,
    borderRadius: 10,
    alignItems: "center",
    justifyContent: "center",
  },

  searchButtonText: {
    color: "#FFFFFF",
    fontWeight: "600",
    fontSize: 13,
  },

  weatherCard: {
    backgroundColor: "#162544",
    borderRadius: 24,
    padding: 22,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: "#273D6B",
  },

  weatherCardTop: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start",
  },

  locationRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
  },

  city: {
    color: "#FFFFFF",
    fontSize: 22,
    fontWeight: "700",
  },

  condition: {
    color: "#94A3B8",
    fontSize: 14,
    fontWeight: "500",
    marginTop: 4,
  },

  weatherCardBottom: {
    marginTop: 24,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-end",
  },

  temperature: {
    color: "#FFFFFF",
    fontSize: 64,
    fontWeight: "300",
    letterSpacing: -2,
  },

  feelsLikeText: {
    color: "#94A3B8",
    fontSize: 14,
    marginBottom: 8,
  },

  detailsRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 24,
  },

  detailCard: {
    backgroundColor: "#16223F",
    width: "31%",
    paddingVertical: 14,
    borderRadius: 16,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#23335A",
  },

  iconContainer: {
    marginBottom: 6,
  },

  detailValue: {
    color: "#FFFFFF",
    fontWeight: "700",
    fontSize: 15,
  },

  detailLabel: {
    color: "#64748B",
    fontSize: 12,
    marginTop: 2,
  },

  sectionHeaderRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 12,
  },

  sectionTitle: {
    color: "#FFFFFF",
    fontSize: 17,
    fontWeight: "700",
    letterSpacing: -0.3,
    marginBottom: 12,
  },

  sectionSubtitle: {
    color: "#60A5FA",
    fontSize: 12,
    fontWeight: "600",
    marginBottom: 12,
  },

  forecastCard: {
    backgroundColor: "#16223F",
    borderRadius: 18,
    padding: 12,
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 24,
    borderWidth: 1,
    borderColor: "#23335A",
  },

  forecastCol: {
    alignItems: "center",
    paddingVertical: 8,
    paddingHorizontal: 10,
    borderRadius: 12,
  },

  forecastColActive: {
    backgroundColor: "#1E2F56",
  },

  forecastDayText: {
    color: "#64748B",
    fontSize: 12,
    fontWeight: "600",
  },

  forecastDayActive: {
    color: "#93C5FD",
  },

  forecastTemp: {
    color: "#FFFFFF",
    fontWeight: "700",
    fontSize: 14,
  },

  chatCard: {
    backgroundColor: "#16223F",
    borderRadius: 20,
    padding: 16,
    marginBottom: 24,
    borderWidth: 1,
    borderColor: "#23335A",
  },

  aiMessage: {
    flexDirection: "row",
    alignItems: "flex-start",
    marginBottom: 12,
    gap: 8,
  },

  userMessage: {
    flexDirection: "row",
    justifyContent: "flex-end",
    marginBottom: 12,
  },

  aiAvatar: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: "#DBEAFE",
    justifyContent: "center",
    alignItems: "center",
    marginTop: 2,
  },

  aiBubble: {
    backgroundColor: "#1F2E52",
    borderRadius: 14,
    borderTopLeftRadius: 4,
    padding: 12,
    maxWidth: "84%",
  },

  userBubble: {
    backgroundColor: "#2563EB",
    borderRadius: 14,
    borderTopRightRadius: 4,
    padding: 12,
    maxWidth: "84%",
  },

  messageText: {
    color: "#FFFFFF",
    lineHeight: 20,
    fontSize: 13,
  },

  chatInputBox: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#0E1830",
    borderRadius: 12,
    paddingHorizontal: 10,
    marginTop: 8,
    borderWidth: 1,
    borderColor: "#1E2D4E",
  },

  chatInput: {
    flex: 1,
    color: "#FFFFFF",
    height: 44,
    fontSize: 13,
  },

  sendButton: {
    width: 32,
    height: 32,
    backgroundColor: "#2563EB",
    borderRadius: 8,
    justifyContent: "center",
    alignItems: "center",
  },

  alertCard: {
    backgroundColor: "#16223F",
    borderRadius: 18,
    padding: 16,
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 24,
    borderWidth: 1,
    borderColor: "#23335A",
    gap: 12,
  },

  alertIconWrapper: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: "rgba(16, 185, 129, 0.1)",
    justifyContent: "center",
    alignItems: "center",
  },

  alertContent: {
    flex: 1,
  },

  alertTitle: {
    color: "#FFFFFF",
    fontWeight: "700",
    fontSize: 14,
  },

  alertText: {
    color: "#94A3B8",
    fontSize: 12,
    marginTop: 3,
    lineHeight: 17,
  },

  climateCard: {
    backgroundColor: "#16223F",
    borderRadius: 18,
    padding: 18,
    marginBottom: 24,
    borderWidth: 1,
    borderColor: "#23335A",
  },

  climateHeader: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    marginBottom: 8,
  },

  climateTitle: {
    color: "#FFFFFF",
    fontWeight: "700",
    fontSize: 15,
  },

  climateText: {
    color: "#94A3B8",
    fontSize: 13,
    lineHeight: 19,
    marginBottom: 14,
  },

  exploreButton: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
  },

  exploreButtonText: {
    color: "#60A5FA",
    fontWeight: "600",
    fontSize: 13,
  },

  footer: {
    textAlign: "center",
    color: "#475569",
    fontSize: 11,
    fontWeight: "500",
    marginTop: 10,
  },
})