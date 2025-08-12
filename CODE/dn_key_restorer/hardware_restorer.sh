#!/bin/bash

# DN-KEY Hardware Restorer
# ========================
# 
# This script helps end users recover bricked DN-KEY devices by:
# 1. Identifying connected devices
# 2. Erasing flash memory
# 3. Flashing TinyUF2 bootloader
# 4. Installing CircuitPython
#
# USAGE:
# 1. Download firmware files from GitHub (see FIRMWARE_FILES section below)
# 2. Update the file paths in this script
# 3. Run: ./hardware_restorer.sh
#
# REQUIREMENTS:
# - macOS or Linux
# - esptool.py (install via: pip install esptool)
# - Firmware files downloaded from GitHub
#
# DISCLAIMER:
# This tool is for educational purposes only. Use at your own risk.
# The authors are not responsible for any damage to your devices.

set -e

# ============================================================================
# FIRMWARE FILES - UPDATE THESE PATHS
# ============================================================================
# Download these files from: https://github.com/deepnetstore/dn_key
#
# 1. TinyUF2 build directory (extract from TinyUF2.zip)
TINYUF2_DIR=""

# 2. CircuitPython UF2 file
CIRCUITPYTHON_UF2=""

# 3. Optional: Test code to verify functionality
TEST_CODE=""

# ============================================================================
# CONFIGURATION
# ============================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${CYAN}[STEP]${NC} $1"; }

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

check_requirements() {
    log_step "Checking requirements..."
    
    # Check if esptool.py is available
    if ! command -v esptool.py >/dev/null 2>&1; then
        log_error "esptool.py not found! Install it with: pip install esptool"
        log_info "Or download from: https://github.com/espressif/esptool"
        exit 1
    fi
    
    # Check firmware files
    if [[ -z "$TINYUF2_DIR" || ! -d "$TINYUF2_DIR" ]]; then
        log_error "TINYUF2_DIR not set or directory not found!"
        log_info "Download TinyUF2 from GitHub and update the path in this script"
        exit 1
    fi
    
    if [[ -z "$CIRCUITPYTHON_UF2" || ! -f "$CIRCUITPYTHON_UF2" ]]; then
        log_error "CIRCUITPYTHON_UF2 not set or file not found!"
        log_info "Download CircuitPython UF2 from GitHub and update the path in this script"
        exit 1
    fi
    
    log_success "All requirements met!"
}

# ============================================================================
# DEVICE DETECTION
# ============================================================================

find_dn_key_devices() {
    log_step "Scanning for DN-KEY devices..."
    
    local devices=()
    local max_scans=3
    local scan_count=0
    
    while [ $scan_count -lt $max_scans ]; do
        ((scan_count++))
        log_info "Scan $scan_count/$max_scans..."
        
        # Find USB devices that match DN-KEY pattern
        for port in /dev/cu.usbmodem*; do
            if [ -e "$port" ]; then
                local port_name=$(basename "$port")
                
                # Check if this looks like a DN-KEY device
                if [[ "$port_name" =~ ^cu\.usbmodem[0-9A-F]+$ ]]; then
                    # Get device identifier
                    local device_id=$(get_device_mac "$port")
                    
                    # Add to devices array if not already present
                    if [[ ! " ${devices[@]} " =~ " $port " ]]; then
                        devices+=("$port")
                        log_info "Found device: $port (ID: $device_id)"
                    fi
                fi
            fi
        done
        
        if [ ${#devices[@]} -gt 0 ]; then
            break
        fi
        
        if [ $scan_count -lt $max_scans ]; then
            log_info "No devices found, retrying in 2 seconds..."
            sleep 2
        fi
    done
    
    if [ ${#devices[@]} -eq 0 ]; then
        log_error "No DN-KEY devices found!"
        log_info "Make sure your device is connected and in download mode"
        log_info "Try double-tapping the reset button on the back of your DN-KEY"
        return 1
    fi
    
    log_success "Found ${#devices[@]} device(s)"
    echo "${devices[@]}"
}

get_device_mac() {
    local device_port="$1"
    local mac=""
    
    # Try to get MAC address using esptool.py
    if mac=$(esptool.py --chip esp32s3 -p "$device_port" chip_id 2>/dev/null | grep "MAC:" | cut -d' ' -f2); then
        echo "$mac"
    else
        # Fallback to port name
        local port_name=$(basename "$device_port")
        echo "port_${port_name}"
    fi
}

# ============================================================================
# FLASHING FUNCTIONS
# ============================================================================

erase_device() {
    local device_port="$1"
    local device_id="$2"
    
    log_step "[$device_id] Erasing flash memory..."
    
    local max_attempts=3
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if [ $attempt -gt 1 ]; then
            log_warning "[$device_id] Erase attempt $attempt/$max_attempts"
            sleep 3
        fi
        
        if esptool.py --chip esp32s3 -p "$device_port" -b 460800 erase_flash; then
            log_success "[$device_id] Flash erased successfully"
            sleep 2
            return 0
        else
            log_error "[$device_id] Flash erase failed (attempt $attempt)"
        fi
        
        ((attempt++))
    done
    
    log_error "[$device_id] Flash erase failed after $max_attempts attempts"
    return 1
}

flash_tinyuf2() {
    local device_port="$1"
    local device_id="$2"
    
    log_step "[$device_id] Flashing TinyUF2 bootloader..."
    
    cd "$TINYUF2_DIR"
    
    local max_attempts=3
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if [ $attempt -gt 1 ]; then
            log_warning "[$device_id] TinyUF2 flash attempt $attempt/$max_attempts"
            sleep 3
        fi
        
        if esptool.py --chip esp32s3 -p "$device_port" -b 460800 write_flash 0x0 bootloader.bin 0x8000 partition-table.bin 0x10000 tinyuf2.bin; then
            log_success "[$device_id] TinyUF2 flashed successfully"
            sleep 3
            return 0
        else
            log_error "[$device_id] TinyUF2 flash failed (attempt $attempt)"
        fi
        
        ((attempt++))
    done
    
    log_error "[$device_id] TinyUF2 flash failed after $max_attempts attempts"
    return 1
}

install_circuitpython() {
    local device_id="$1"
    
    log_step "[$device_id] Installing CircuitPython..."
    
    # Wait for DN_BOOT volume to appear
    local max_wait=30
    local wait_count=0
    
    while [ $wait_count -lt $max_wait ]; do
        if [ -d "/Volumes/DN_BOOT" ]; then
            log_success "[$device_id] DN_BOOT volume detected"
            break
        fi
        
        ((wait_count++))
        log_info "[$device_id] Waiting for DN_BOOT volume... ($wait_count/$max_wait)"
        sleep 1
    done
    
    if [ ! -d "/Volumes/DN_BOOT" ]; then
        log_error "[$device_id] DN_BOOT volume not detected after $max_wait seconds"
        return 1
    fi
    
    # Copy CircuitPython UF2 to DN_BOOT
    if cp "$CIRCUITPYTHON_UF2" "/Volumes/DN_BOOT/"; then
        log_success "[$device_id] CircuitPython UF2 copied to DN_BOOT"
        
        # Wait for device to reboot and appear as DN-S3-PY
        local max_wait=30
        local wait_count=0
        
        while [ $wait_count -lt $max_wait ]; do
            if [ -d "/Volumes/DN-S3-PY" ]; then
                log_success "[$device_id] DN-S3-PY volume detected - CircuitPython installed!"
                return 0
            fi
            
            ((wait_count++))
            log_info "[$device_id] Waiting for DN-S3-PY volume... ($wait_count/$max_wait)"
            sleep 1
        done
        
        log_error "[$device_id] DN-S3-PY volume not detected after $max_wait seconds"
        return 1
    else
        log_error "[$device_id] Failed to copy CircuitPython UF2 to DN_BOOT"
        return 1
    fi
}

install_test_code() {
    local device_id="$1"
    
    if [[ -n "$TEST_CODE" && -f "$TEST_CODE" ]]; then
        log_step "[$device_id] Installing test code..."
        
        if cp "$TEST_CODE" "/Volumes/DN-S3-PY/code.py"; then
            log_success "[$device_id] Test code installed successfully"
        else
            log_warning "[$device_id] Failed to install test code"
        fi
    fi
}

# ============================================================================
# MAIN RESTORATION PROCESS
# ============================================================================

restore_device() {
    local device_port="$1"
    local device_id="$2"
    
    log_step "Starting restoration for device: $device_id"
    
    # Step 1: Erase flash
    if ! erase_device "$device_port" "$device_id"; then
        log_error "[$device_id] Restoration failed at erase step"
        return 1
    fi
    
    # Step 2: Flash TinyUF2
    if ! flash_tinyuf2 "$device_port" "$device_id"; then
        log_error "[$device_id] Restoration failed at TinyUF2 step"
        return 1
    fi
    
    # Step 3: Install CircuitPython
    if ! install_circuitpython "$device_id"; then
        log_error "[$device_id] Restoration failed at CircuitPython step"
        return 1
    fi
    
    # Step 4: Install test code (optional)
    install_test_code "$device_id"
    
    log_success "[$device_id] Device restoration completed successfully!"
}

# ============================================================================
# MAIN SCRIPT
# ============================================================================

main() {
    echo -e "${CYAN}"
    echo "=========================================="
    echo "    DN-KEY Hardware Restorer"
    echo "=========================================="
    echo -e "${NC}"
    
    log_info "This tool will help you restore bricked DN-KEY devices"
    log_info "Make sure you have downloaded the required firmware files"
    echo
    
    # Check requirements
    check_requirements
    echo
    
    # Find devices
    local devices
    if ! devices=($(find_dn_key_devices)); then
        exit 1
    fi
    echo
    
    # Confirm with user
    log_warning "Found ${#devices[@]} device(s) to restore:"
    for device in "${devices[@]}"; do
        local device_id=$(get_device_mac "$device")
        log_info "  - $device (ID: $device_id)"
    done
    echo
    
    read -p "Do you want to proceed with restoration? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Restoration cancelled by user"
        exit 0
    fi
    echo
    
    # Restore each device
    local success_count=0
    for device in "${devices[@]}"; do
        local device_id=$(get_device_mac "$device")
        
        log_step "Processing device: $device_id"
        
        if restore_device "$device" "$device_id"; then
            ((success_count++))
        else
            log_error "Failed to restore device: $device_id"
        fi
        
        echo
    done
    
    # Summary
    echo -e "${CYAN}=========================================="
    echo "    RESTORATION SUMMARY"
    echo "=========================================="
    echo -e "${NC}"
    
    if [ $success_count -eq ${#devices[@]} ]; then
        log_success "All ${#devices[@]} device(s) restored successfully!"
    elif [ $success_count -gt 0 ]; then
        log_warning "$success_count of ${#devices[@]} device(s) restored successfully"
        log_error "$((${#devices[@]} - success_count)) device(s) failed"
    else
        log_error "No devices were restored successfully"
    fi
    
    echo
    log_info "Your DN-KEY device(s) should now be working!"
    log_info "Check the /Volumes/DN-S3-PY drive for the CircuitPython volume"
}

# Run main function
main "$@"
