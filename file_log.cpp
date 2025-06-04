// file_log.cpp - C++ version of file_log.py
#include <iostream>
#include <filesystem>
#include <iomanip>
#include <chrono>
#include <map>
#include <string>

namespace fs = std::filesystem;

// File icons by extension
std::map<std::string, std::string> FILE_ICONS = {
    {".py", "🐍"}, {".csv", "📊"}, {".md", "📝"}, {".txt", "📝"},
    {".jpg", "🖼️"}, {".jpeg", "🖼️"}, {".png", "🖼️"}, {".gif", "🖼️"},
    {".pdf", "📄"}, {".zip", "📦"}, {".tar", "📦"}, {".gz", "📦"}
};

std::string format_size(uintmax_t bytes) {
    const char* units[] = {"B", "KB", "MB", "GB", "TB", "PB"};
    double size = bytes;
    int unit_index = 0;
    while (size >= 1024 && unit_index < 5) {
        size /= 1024;
        ++unit_index;
    }
    std::ostringstream oss;
    oss << std::fixed << std::setprecision(2) << size << " " << units[unit_index];
    return oss.str();
}

std::string format_date(const std::filesystem::file_time_type& ftime) {
    auto sctp = std::chrono::time_point_cast<std::chrono::system_clock::duration>(ftime - fs::file_time_type::clock::now()
                            + std::chrono::system_clock::now());
    std::time_t cftime = std::chrono::system_clock::to_time_t(sctp);
    std::ostringstream oss;
    oss << std::put_time(std::localtime(&cftime), "%Y-%m-%d %H:%M:%S");
    return oss.str();
}

std::string get_file_icon(const std::string& filename) {
    std::string ext = fs::path(filename).extension().string();
    for (auto& c : ext) c = tolower(c);
    return FILE_ICONS.count(ext) ? FILE_ICONS[ext] : "📄";
}

void scan_directory_recursive(const std::string& directory) {
    std::cout << "\n📂 Scanning directory: " << fs::absolute(directory) << "\n";
    std::cout << std::string(90, '=') << "\n";

    for (const auto& entry : fs::recursive_directory_iterator(directory)) {
        std::string indent(entry.depth() * 4, ' ');
        if (entry.is_directory()) {
            std::cout << indent << "📁 " << entry.path().filename().string() << "/\n";
        } else {
            try {
                std::string icon = get_file_icon(entry.path().string());
                std::string size = format_size(fs::file_size(entry.path()));
                std::string modified = format_date(fs::last_write_time(entry.path()));
                std::cout << indent << icon << " " << entry.path().filename().string()
                          << " - " << size << " - " << modified << "\n";
            } catch (const std::exception& e) {
                std::cerr << indent << "⚠️ " << entry.path().filename().string()
                          << " (Error: " << e.what() << ")\n";
            }
        }
    }
    std::cout << "\n🌲 Scan complete!\n";
}

int main() {
    std::string path;
    std::cout << "Enter directory path (press Enter for current directory): ";
    std::getline(std::cin, path);
    if (path.empty()) path = ".";
    scan_directory_recursive(path);
    return 0;
}
