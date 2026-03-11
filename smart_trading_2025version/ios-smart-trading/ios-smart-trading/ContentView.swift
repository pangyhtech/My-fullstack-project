//
//  ContentView.swift
//  ios-smart-trading
//
//  Created by mc on 2025/5/19.
//

import SwiftUI

struct ContentView: View {
    @EnvironmentObject var exchangeDataStore: ExchangeDataStore
    
    var body: some View {
        NavigationView {
            SmartTradingView()
                .navigationBarHidden(true)
                .environmentObject(exchangeDataStore)
        }
    }
}

#Preview {
    ContentView()
        .environmentObject(ExchangeDataStore())
}
