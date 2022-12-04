import { useState, useEffect, useRef } from 'react'
import MapView, { PROVIDER_GOOGLE, Circle } from 'react-native-maps'
import { StyleSheet, View, Text, TouchableHighlight } from 'react-native'
import { registerRootComponent } from 'expo'
import modes from "modes.json"
import * as Location from 'expo-location'
import lotsData from "data.json"

function App() {
  const [location, setLocation] = useState(null)
  const [errorMsg, setErrorMsg] = useState(null)
  const mapRef = useRef(null)
  const [lots, setLots] = useState(lotsData)

  useEffect(() => {
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync()
      if (status !== 'granted') {
        return
      }

      let location = await Location.getCurrentPositionAsync({ accuracy: Platform.OS == 'android' ? Location.Accuracy.Low : Location.Accuracy.Lowest, })
      setLocation(location)

      if (mapRef.current) {
        mapRef.current.animateToRegion({
          longitude: location.coords.longitude,
          latitude: location.coords.latitude,
          longitudeDelta: 0.005,
          latitudeDelta: 0.005
        }, 2000)
      }
    })()
  }, [])

  const randomizeOccupany = () => {
    const newLots = [...lots]

    for (let i = Math.floor(Math.random() * 4); i >= 0; i--) {
      const index = Math.floor(Math.random() * lots.length)

      newLots[index].occupancy = newLots[index].occupancy == "free" ? "taken" : "free"
    }

    setLots(newLots)
  }

  return (
    <View style={styles.container}>
      <MapView
        onPress={randomizeOccupany}
        ref={mapRef}
        provider={PROVIDER_GOOGLE}
        style={styles.map}
        customMapStyle={modes.dark}
        initialRegion={{
          latitude: 48.71,
          longitude: 21.255,
          latitudeDelta: 0.1,
          longitudeDelta: 0.1
        }}
        showsUserLocation={location != null}
        rotateEnabled={false}
        loadingEnabled
      >
        {
          lots.map((lot, i) =>
            <Circle
              key={i}
              center={{
                longitude: lot.location[0],
                latitude: lot.location[1]
              }}
              radius={1}
              strokeWidth={0}
              strokeColor="rgba(0,0,0,0)"
              fillColor={lot.occupancy == "free" ? "#00FF00" : lot.occupancy == "taken" ? "#FF0000" : "#232323"}
            />
          )
        }
      </MapView>

      {/*
      <TouchableHighlight onPress={() => { }}>
        <>
          <View><Text>HMM</Text></View>
          <MaterialIcons name="my-location" size={24} color="black" style={styles.locationButton} />
        </>
      </TouchableHighlight>
        */}

      <View style={styles.main}>
        <Text style={styles.belowText}>Free parking spaces</Text>
        <Text style={styles.freeSpaces}>12</Text>
      </View>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    position: "relative"
  },
  map: {
    width: '100%',
    height: '90%'
  },
  main: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 30,
    width: "100%",
    height: "14%",
    position: "absolute",
    bottom: 0,
    left: 0,
    backgroundColor: "white",
    borderRadius: 15,
    shadowColor: '#171717',
    shadowOffset: { width: 0, height: -10 },
    shadowOpacity: 0.3,
    shadowRadius: 6,
  },
  belowText: {
    fontSize: 18,
    color: "#6D6D6D",
    textTransform: 'uppercase',
    letterSpacing: 2
  },
  freeSpaces: {
    backgroundColor: "#49ADE1",
    display: "flex",
    paddingHorizontal: 16,
    paddingVertical: 8,
    color: "white",
    fontSize: 24
  },
  locationButton: {
    width: 5,
    height: 5,
    backgroundColor: "red",
    zIndex: 1000,
    borderRadius: "100%",
    position: "absolute",
    right: 4,
    bottom: "22%"
  }
})


export default registerRootComponent(App)