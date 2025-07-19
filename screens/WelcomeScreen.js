import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Dimensions, StatusBar } from 'react-native';
import Video from 'react-native-video';

const { width, height } = Dimensions.get('window');

const WelcomeScreen = ({ navigation }) => {
  const [signInMode, setSignInMode] = useState(false);

  return (
    <View style={styles.container}>
      <StatusBar
        barStyle="light-content"
        backgroundColor="transparent"
        translucent={true}
      />
      <Video
        source={require('../assets/welcome-bg.mp4')}
        style={styles.backgroundVideo}
        resizeMode="cover"
        repeat
        muted
        rate={1.0}
        ignoreSilentSwitch="obey"
      />
      <View style={styles.overlay}>
        <View style={styles.centerContent}>
          <View style={styles.appNameContainer}>
            <Text style={styles.appNameZoo}>Zoo</Text>
            <Text style={styles.appNameBae}>bae</Text>
          </View>
          <Text style={styles.tagline}>Your AI Matchmaker</Text>
        </View>
        <View style={styles.bottomButtons}>
          {!signInMode ? (
            <>
              <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Register')}>
                <Text style={styles.buttonText}>Create Account</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.signInButton} onPress={() => setSignInMode(true)}>
                <Text style={styles.signInText}>Sign In</Text>
              </TouchableOpacity>
            </>
          ) : (
            <>
              <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Login')}>
                <Text style={styles.buttonText}>Sign in with email</Text>
              </TouchableOpacity>
              <TouchableOpacity style={[styles.button, styles.phoneButton]} onPress={() => {/* TODO: Implement phone sign in */}}>
                <Text style={styles.buttonText}>Sign in with phone number</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.backButton} onPress={() => setSignInMode(false)}>
                <Text style={styles.backText}>Back</Text>
              </TouchableOpacity>
            </>
          )}
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    width: width,
    height: height,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#000',
  },
  backgroundVideo: {
    position: 'absolute',
    top: 0,
    left: 0,
    width: width,
    height: height + 50,
    zIndex: 0,
  },
  overlay: {
    flex: 1,
    width: '100%',
    height: '100%',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.3)',
    zIndex: 1,
    paddingTop: 50,
    paddingBottom: 40,
  },
  centerContent: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  appNameContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  appNameZoo: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#fff',
    letterSpacing: 2,
    textShadowColor: '#000',
    textShadowOffset: { width: 2, height: 2 },
    textShadowRadius: 8,
  },
  appNameBae: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#FF69B4',
    letterSpacing: 2,
    textShadowColor: '#000',
    textShadowOffset: { width: 2, height: 2 },
    textShadowRadius: 8,
  },
  tagline: {
    fontSize: 22,
    color: '#fff',
    fontStyle: 'italic',
    textAlign: 'center',
    textShadowColor: '#000',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 6,
  },
  bottomButtons: {
    position: 'absolute',
    bottom: 40,
    width: '100%',
    flexDirection: 'column',
    alignItems: 'center',
  },
  button: {
    backgroundColor: 'rgba(255,255,255,0.85)',
    paddingVertical: 16,
    paddingHorizontal: 32,
    borderRadius: 30,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 5,
  },
  buttonText: {
    color: '#222',
    fontSize: 18,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
  signInButton: {
    backgroundColor: 'transparent',
    paddingVertical: 12,
    paddingHorizontal: 32,
    borderRadius: 30,
  },
  signInText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    letterSpacing: 1,
    textShadowColor: '#000',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 4,
  },
  backButton: {
    backgroundColor: 'transparent',
    paddingVertical: 12,
    paddingHorizontal: 32,
    borderRadius: 30,
    marginTop: 8,
  },
  backText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    letterSpacing: 1,
    textShadowColor: '#000',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 4,
  },
  phoneButton: {
    backgroundColor: '#FFB7C5', // cherry blossom
  },
});

export default WelcomeScreen; 