import React from 'react';
import { View, Text, StyleSheet, Dimensions, StatusBar } from 'react-native';

const { width, height } = Dimensions.get('window');

const TBDScreen = () => {
  return (
    <View style={styles.container}>
      <StatusBar
        barStyle="light-content"
        backgroundColor="transparent"
        translucent={true}
      />
      <View style={styles.content}>
        <Text style={styles.title}>Coming Soon</Text>
        <Text style={styles.subtitle}>New features are on the way</Text>
        <View style={styles.placeholder}>
          <Text style={styles.placeholderText}>TBD</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    width: width,
    height: height + 50,
    backgroundColor: '#FFF0F5',
    paddingTop: 50,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FF69B4',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 18,
    color: '#FFB7C5',
    marginBottom: 40,
    textAlign: 'center',
  },
  placeholder: {
    width: 200,
    height: 200,
    backgroundColor: '#FFE4E1',
    borderRadius: 100,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#FFB7C5',
    borderStyle: 'dashed',
  },
  placeholderText: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#FF69B4',
  },
});

export default TBDScreen; 