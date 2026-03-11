//
//  ios_smart_tradingApp.swift
//  ios-smart-trading
//
//  Created by mc on 2025/5/19.
//

import SwiftUI

@main
struct ios_smart_tradingApp: App {
    @StateObject private var exchangeDataStore = ExchangeDataStore()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(exchangeDataStore)
                .preferredColorScheme(.dark)
        }
    }
}
