const { User } = require("../model");

// 用户登录
exports.login = async (req, res, next) => {
    try {
        res.send("Post User Login");
    } catch (err) {
        next(err);
    }
};
// 用户注册
exports.register = async (req, res, next) => {
    try {
        // 1. 获取请求数据
        console.log(req.body);

        // 2.数据验证
        // 2.1 基本验证 参数是否通过
        // 2.2 业务验证 不能重复等

        const user = new User(req.body.user);

        // 3. 保存到数据库
        await user.save();

        // 4. 发送成功响应
        res.status(201).json({
            user,
        });
    } catch (err) {
        next(err);
    }
};
// 获取用户
exports.getCurrentUser = async (req, res, next) => {
    try {
        const a = JSON.parse(1 / 0);
        console.log(a);
        res.send("GET User");
    } catch (err) {
        next(err);
    }
};
// 更新用户
exports.updateCurrentUser = async (req, res, next) => {
    try {
        res.send("Post User Login");
    } catch (err) {
        next(err);
    }
};
