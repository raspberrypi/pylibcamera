#include <iostream>
#include <libcamera/camera_manager.h>


int main()
{
    std::cout << libcamera::CameraManager::version() << "\n";
}