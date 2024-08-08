#include <iostream>
#include <thread>
#include <vector>
#include <wiringPiI2C.h>
#include "edge-impulse-sdk/classifier/ei_run_classifier.h"

// ADXL345 Accelerometer registers
#define ADXL345_ADDR 0x53
#define ADXL345_POWER_CTL 0x2D
#define ADXL345_DATAX0 0x32

// Function to initialize the ADXL345 accelerometer
int init_accelerometer() {
    int fd = wiringPiI2CSetup(ADXL345_ADDR);
    if (fd == -1) {
        std::cerr << "Failed to initialize I2C device" << std::endl;
        exit(1);
    }
    // Wake up the accelerometer
    wiringPiI2CWriteReg8(fd, ADXL345_POWER_CTL, 0x08);
    return fd;
}

// Function to read accelerometer data
std::vector<float> read_accelerometer(int fd) {
    int16_t x, y, z;
    x = wiringPiI2CReadReg16(fd, ADXL345_DATAX0);
    y = wiringPiI2CReadReg16(fd, ADXL345_DATAX0 + 2);
    z = wiringPiI2CReadReg16(fd, ADXL345_DATAX0 + 4);

    // Convert the readings to Gs (assuming +/- 2g range)
    float scale_factor = 0.004;
    std::vector<float> accel_data = {x * scale_factor, y * scale_factor, z * scale_factor};
    return accel_data;
}

// Callback function to provide signal data for the classifier
static int get_signal_data(size_t offset, size_t length, float *out_ptr) {
    std::copy(input_buf + offset, input_buf + offset + length, out_ptr);
    return EIDSP_OK;
}

// Input buffer for inference
static float input_buf[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE] = {};

int main() {
    // Initialize the accelerometer
    int fd = init_accelerometer();

    // Acquire a single sample from the accelerometer
    std::vector<float> accel_data = read_accelerometer(fd);

    // Fill the input buffer with the acquired sample
    for (size_t i = 0; i < accel_data.size(); ++i) {
        input_buf[i] = accel_data[i];
    }

    // Set up the signal struct for the classifier
    signal_t signal;
    signal.total_length = EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE;
    signal.get_data = &get_signal_data;

    // Perform inference
    ei_impulse_result_t result;
    EI_IMPULSE_ERROR res = run_classifier(&signal, &result, false);

    // Print the inference results
    std::cout << "run_classifier returned: " << res << std::endl;
    std::cout << "Timing: DSP " << result.timing.dsp << " ms, inference " << result.timing.classification << " ms, anomaly " << result.timing.anomaly << " ms" << std::endl;

    // Print the prediction results (classification)
    std::cout << "Predictions:" << std::endl;
    for (uint16_t i = 0; i < EI_CLASSIFIER_LABEL_COUNT; i++) {
        std::cout << "  " << ei_classifier_inferencing_categories[i] << ": " << result.classification[i].value << std::endl;
    }

    // Print the anomaly result (if available)
    #if EI_CLASSIFIER_HAS_ANOMALY == 1
    std::cout << "Anomaly prediction: " << result.anomaly << std::endl;
    #endif

    return 0;
}
