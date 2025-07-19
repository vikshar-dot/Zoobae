import React, { useState, useMemo, useEffect, useRef } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert, TouchableOpacity, ImageBackground, Dimensions, Animated, StatusBar } from 'react-native';
import axios from 'axios';

const bgImages = [
  require('../assets/bg1.jpg'),
  require('../assets/bg2.jpg'),
  require('../assets/bg3.jpg'),
  require('../assets/bg4.jpg'),
  require('../assets/bg5.jpg'),
  require('../assets/bg6.jpg'),
];

const { width, height } = Dimensions.get('window');

const taglines = [
  'Your AI Matchmaker',
  'Modern dating',
  'Modern Matching',
];

const LoginScreen = ({ navigation }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [taglineIndex, setTaglineIndex] = useState(0);
  const fadeAnim = useRef(new Animated.Value(1)).current;
  const scaleAnim = useRef(new Animated.Value(1)).current;

  const bgImage = useMemo(() => {
    const idx = Math.floor(Math.random() * bgImages.length);
    return bgImages[idx];
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      // Gentle fade and scale
      Animated.parallel([
        Animated.timing(fadeAnim, {
          toValue: 0,
          duration: 800,
          useNativeDriver: true,
        }),
        Animated.timing(scaleAnim, {
          toValue: 0.95,
          duration: 800,
          useNativeDriver: true,
        }),
      ]).start(() => {
        setTaglineIndex((prev) => (prev + 1) % taglines.length);
        // Gentle fade and scale back
        Animated.parallel([
          Animated.timing(fadeAnim, {
            toValue: 1,
            duration: 800,
            useNativeDriver: true,
          }),
          Animated.timing(scaleAnim, {
            toValue: 1,
            duration: 800,
            useNativeDriver: true,
          }),
        ]).start();
      });
    }, 5000);
    return () => clearInterval(interval);
  }, [fadeAnim, scaleAnim]);

  const handleLogin = async () => {
    setLoading(true);
    try {
      const form = new FormData();
      form.append('username', email);
      form.append('password', password);
      await axios.post('http://192.168.1.8:8000/login', form, { headers: { 'Content-Type': 'multipart/form-data' } });
      setLoading(false);
      navigation.replace('MainTabs');
    } catch (err) {
      setLoading(false);
      Alert.alert('Login failed', err?.response?.data?.detail || 'Unknown error');
    }
  };

  return (
    <ImageBackground source={bgImage} style={styles.background} resizeMode="cover">
      <StatusBar
        barStyle="light-content"
        backgroundColor="transparent"
        translucent={true}
      />
      <View style={styles.bottomContainer}>
        <View style={styles.branding}>
          <View style={styles.appNameContainer}>
            <Text style={styles.appNameZoo}>Zoo</Text>
            <Text style={styles.appNameBae}>bae</Text>
          </View>
          <Animated.Text style={[styles.tagline, { opacity: fadeAnim, transform: [{ scale: scaleAnim }] }]}>
            {taglines[taglineIndex]}
          </Animated.Text>
        </View>
        <View style={styles.inputsBlock}>
          <TextInput
            style={[styles.input, { color: '#000' }]}
            placeholder="Email"
            value={email}
            onChangeText={setEmail}
            autoCapitalize="none"
            keyboardType="email-address"
            placeholderTextColor="#555"
          />
          <TextInput
            style={[styles.input, { color: '#000' }]}
            placeholder="Password"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
            placeholderTextColor="#555"
          />
          <TouchableOpacity style={styles.loginButton} onPress={handleLogin} disabled={loading}>
            <Text style={styles.loginButtonText}>{loading ? 'Logging in...' : 'Login'}</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={() => navigation.replace('Register')} style={styles.link}>
            <Text style={styles.linkText}>Don't have an account? Register</Text>
          </TouchableOpacity>
        </View>
      </View>
    </ImageBackground>
  );
};

const styles = StyleSheet.create({
  background: {
    flex: 1,
    width: width,
    height: height + 50,
    justifyContent: 'center',
    alignItems: 'center',
  },
  bottomContainer: {
    position: 'absolute',
    bottom: 0,
    width: '100%',
    alignItems: 'center',
    paddingBottom: 40,
    paddingTop: 50,
  },
  branding: {
    alignItems: 'center',
    marginBottom: 32,
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
    fontSize: 18,
    color: '#fff',
    textAlign: 'center',
    textShadowColor: '#000',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 6,
  },
  inputsBlock: {
    width: '100%',
    alignItems: 'center',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    paddingVertical: 18,
    paddingHorizontal: 20,
    marginBottom: 20,
    fontSize: 18,
    color: '#000',
    backgroundColor: '#fff',
    width: 300,
    maxWidth: '90%',
  },
  loginButton: {
    backgroundColor: '#FF69B4',
    borderRadius: 8,
    marginTop: 8,
    marginBottom: 8,
    width: 300,
    maxWidth: '90%',
    overflow: 'hidden',
  },
  loginButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 18,
    textAlign: 'center',
    paddingVertical: 14,
  },
  link: { marginTop: 20, alignItems: 'center' },
  linkText: { color: '#fff', fontWeight: 'bold', fontSize: 16 },
});

export default LoginScreen; 