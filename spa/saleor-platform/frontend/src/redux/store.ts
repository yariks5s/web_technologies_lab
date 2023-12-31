import { configureStore } from '@reduxjs/toolkit';
import authReducer from './auth.slice';
import storage from 'redux-persist/lib/storage';
import { persistReducer, persistStore } from 'redux-persist';


const persistConfig = {
  key: 'auth',
  storage
}

export const store = configureStore({
  reducer: {auth: persistReducer(persistConfig, authReducer)},
  middleware: (getDefaultMiddleware)=> getDefaultMiddleware({serializableCheck: false}),
});

export const persistor = persistStore(store)

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch